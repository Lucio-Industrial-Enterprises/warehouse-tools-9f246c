import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (unchanged behaviour)
    # ------------------------------------------------------------------
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit(self):
        """Passing service='standard' must equal the default."""
        self.assertEqual(
            shipping_quote(3, "local", "standard"),
            shipping_quote(3, "local"),
        )

    # ------------------------------------------------------------------
    # Express service (+$7 flat surcharge)
    # ------------------------------------------------------------------
    def test_express_local(self):
        # 5.0 (local base) + 7.0 (express) + 1.5 * 2 = 15.0
        self.assertEqual(shipping_quote(2, "local", "express"), 15.0)

    def test_express_regional(self):
        # 8.0 (regional base) + 7.0 (express) + 1.5 * 2 = 18.0
        self.assertEqual(shipping_quote(2, "regional", "express"), 18.0)

    def test_express_surcharge_is_seven(self):
        """Express should always cost exactly $7 more than standard."""
        for zone in ("local", "regional"):
            with self.subTest(zone=zone):
                diff = shipping_quote(5, zone, "express") - shipping_quote(5, zone, "standard")
                self.assertAlmostEqual(diff, 7.0)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "intergalactic")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", "overnight")
