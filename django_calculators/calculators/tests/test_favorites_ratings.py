"""
Audit tests for favourite calculators (per-user pinned tools + ordering) and
calculator ratings (1–5 stars + comment), including ownership isolation and
input validation.
"""

from django.test import override_settings
from .base import BaseAPITestCase, NO_THROTTLE_RF

FAV = '/api/calculators/my/favorites/'
RATE = '/api/calculators/ratings/'


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class FavoriteTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('fav@example.com')
        self.login_as(self.user)

    def test_add_and_list(self):
        self.assertEqual(self.client.post(FAV, {'calculator_id': 'salary'}, format='json').status_code, 201)
        self.client.post(FAV, {'calculator_id': 'bmi'}, format='json')
        data = self.client.get(FAV).json()['data']
        self.assertEqual([f['calculator_id'] for f in data], ['salary', 'bmi'])

    def test_add_is_idempotent(self):
        self.client.post(FAV, {'calculator_id': 'salary'}, format='json')
        again = self.client.post(FAV, {'calculator_id': 'salary'}, format='json')
        self.assertEqual(again.status_code, 200)  # not a duplicate
        self.assertEqual(len(self.client.get(FAV).json()['data']), 1)

    def test_reorder(self):
        for cid in ['salary', 'bmi', 'vat']:
            self.client.post(FAV, {'calculator_id': cid}, format='json')
        resp = self.client.post(f'{FAV}reorder/', {'order': ['vat', 'salary', 'bmi']}, format='json')
        self.assertEqual(resp.status_code, 200)
        data = self.client.get(FAV).json()['data']
        self.assertEqual([f['calculator_id'] for f in data], ['vat', 'salary', 'bmi'])

    def test_remove(self):
        self.client.post(FAV, {'calculator_id': 'salary'}, format='json')
        self.assertEqual(self.client.delete(f'{FAV}salary/').status_code, 200)
        self.assertEqual(self.client.get(FAV).json()['data'], [])

    def test_remove_missing_404(self):
        self.assertEqual(self.client.delete(f'{FAV}nope/').status_code, 404)

    def test_anonymous_blocked(self):
        self.logout()
        self.assertEqual(self.client.get(FAV).status_code, 401)
        self.assertEqual(self.client.post(FAV, {'calculator_id': 'salary'}, format='json').status_code, 401)

    def test_favorites_are_per_user(self):
        self.client.post(FAV, {'calculator_id': 'salary'}, format='json')
        other = self.make_user('other@example.com')
        self.login_as(other)
        self.assertEqual(self.client.get(FAV).json()['data'], [])


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class RatingTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('rater@example.com', first_name='Ann')

    def test_public_can_read_empty_aggregate(self):
        resp = self.client.get(f'{RATE}?calculator_id=salary')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body['count'], 0)
        self.assertEqual(body['average'], 0)

    def test_get_requires_calculator_id(self):
        self.assertEqual(self.client.get(RATE).status_code, 400)

    def test_submit_and_aggregate(self):
        self.login_as(self.user)
        resp = self.client.post(RATE, {'calculator_id': 'salary', 'rating': 5, 'comment': 'super'}, format='json')
        self.assertEqual(resp.status_code, 201)
        other = self.make_user('o@example.com')
        self.login_as(other)
        self.client.post(RATE, {'calculator_id': 'salary', 'rating': 3, 'comment': 'ok'}, format='json')
        agg = self.client.get(f'{RATE}?calculator_id=salary').json()
        self.assertEqual(agg['count'], 2)
        self.assertEqual(agg['average'], 4.0)
        self.assertEqual(len(agg['recent']), 2)

    def test_resubmit_updates_not_duplicates(self):
        self.login_as(self.user)
        self.client.post(RATE, {'calculator_id': 'salary', 'rating': 5}, format='json')
        resp = self.client.post(RATE, {'calculator_id': 'salary', 'rating': 2}, format='json')
        self.assertEqual(resp.status_code, 200)  # update, not create
        agg = self.client.get(f'{RATE}?calculator_id=salary').json()
        self.assertEqual(agg['count'], 1)
        self.assertEqual(agg['average'], 2.0)

    def test_rating_out_of_range_rejected(self):
        self.login_as(self.user)
        self.assertEqual(self.client.post(RATE, {'calculator_id': 'salary', 'rating': 9}, format='json').status_code, 400)
        self.assertEqual(self.client.post(RATE, {'calculator_id': 'salary', 'rating': 0}, format='json').status_code, 400)

    def test_anonymous_cannot_submit(self):
        self.assertEqual(self.client.post(RATE, {'calculator_id': 'salary', 'rating': 5}, format='json').status_code, 401)

    def test_my_rating_returned_for_owner_only(self):
        self.login_as(self.user)
        self.client.post(RATE, {'calculator_id': 'salary', 'rating': 4}, format='json')
        self.assertEqual(self.client.get(f'{RATE}?calculator_id=salary').json()['my_rating']['rating'], 4)
        # Anonymous read has no my_rating.
        self.logout()
        self.assertIsNone(self.client.get(f'{RATE}?calculator_id=salary').json()['my_rating'])

    def test_author_name_is_privacy_light(self):
        # No first name -> masked email local part, never the full address.
        u = self.make_user('secretmail@example.com')
        self.login_as(u)
        self.client.post(RATE, {'calculator_id': 'salary', 'rating': 5, 'comment': 'hi'}, format='json')
        author = self.client.get(f'{RATE}?calculator_id=salary').json()['recent'][0]['author']
        self.assertNotIn('@', author)
        self.assertNotIn('secretmail', author)
