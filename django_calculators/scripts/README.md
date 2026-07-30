# Manual dev scripts

These are **ad-hoc print-scripts** for manual verification — NOT part of the
automated test suite (that lives in `calculators/tests/` and `users/tests/`).
They were moved out of the project root so they aren't mistaken for tests or
collected by broad test runners.

Run from the `django_calculators/` directory with the Django environment set up,
e.g.:

```bash
python -m scripts.test_calc
```

They read rates from `calculators/services/config_variables.py`, which now loads
from the editable data files in `calculators/services/data/`.
