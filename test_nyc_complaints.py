import argparse
import unittest
from types import SimpleNamespace

from nyc_complaints import (
    int_between,
    validate_zip_code,
    validate_borough,
    create_params,
)


class TestValidation(unittest.TestCase):
    def test_validate_borough_accepts_lowercase(self):
        self.assertEqual(validate_borough("brooklyn"), "BROOKLYN")

    def test_validate_borough_accepts_extra_spaces(self):
        self.assertEqual(validate_borough("  queens  "), "QUEENS")

    def test_validate_borough_rejects_invalid_borough(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_borough("JERSEY")

    def test_validate_zip_code_accepts_five_digits(self):
        self.assertEqual(validate_zip_code("10451"), "10451")

    def test_validate_zip_code_rejects_short_zip(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_zip_code("1045")

    def test_validate_zip_code_rejects_letters(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_zip_code("abcde")

    def test_int_between_accepts_valid_number(self):
        checker = int_between(2, 365)
        self.assertEqual(checker("30"), 30)

    def test_int_between_rejects_too_small_number(self):
        checker = int_between(2, 365)
        with self.assertRaises(argparse.ArgumentTypeError):
            checker("1")

    def test_int_between_rejects_too_large_number(self):
        checker = int_between(2, 365)
        with self.assertRaises(argparse.ArgumentTypeError):
            checker("366")


class TestCreateParams(unittest.TestCase):
    def test_create_params_with_borough(self):
        args = SimpleNamespace(
            borough="BROOKLYN",
            zip_code=None,
            days=7,
            top=10,
            min_count=1,
        )

        params = create_params(args)

        self.assertEqual(
            params["$select"],
            "complaint_type, count(*) AS count",
        )
        self.assertIn("created_date >=", params["$where"])
        self.assertIn("borough = 'BROOKLYN'", params["$where"])
        self.assertNotIn("incident_zip", params["$where"])
        self.assertEqual(params["$group"], "complaint_type HAVING count >= 1")
        self.assertEqual(params["$order"], "count DESC")
        self.assertEqual(params["$limit"], 10)

    def test_create_params_with_zip_code(self):
        args = SimpleNamespace(
            borough=None,
            zip_code="10451",
            days=7,
            top=None,
            min_count=5,
        )

        params = create_params(args)

        self.assertIn("incident_zip = '10451'", params["$where"])
        self.assertNotIn("borough =", params["$where"])
        self.assertEqual(params["$group"], "complaint_type HAVING count >= 5")
        self.assertNotIn("$limit", params)


if __name__ == "__main__":
    unittest.main()
