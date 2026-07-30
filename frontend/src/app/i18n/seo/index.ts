import { Locale } from '../locales';
import { SeoEntry, SeoContentMap } from './types';
import { SEO_BATCH_A } from './batch-a';
import { SEO_BATCH_B } from './batch-b';
import { SEO_BATCH_C } from './batch-c';

/**
 * Localized per-page SEO content (title, description, keywords, FAQ) for the
 * calculators. Split into batch files so they are easy to author/review;
 * merged here. Each calculator reads its entry via getSeoContent() and feeds it
 * to SeoService.apply() together with its path.
 */
const ALL: SeoContentMap = { ...SEO_BATCH_A, ...SEO_BATCH_B, ...SEO_BATCH_C };

/** Localized SEO content for a page id, falling back to Slovak then empty. */
export function getSeoContent(id: string, locale: Locale): SeoEntry {
  const entry = ALL[id];
  if (!entry) return { title: '', description: '' };
  return entry[locale] ?? entry.sk;
}
