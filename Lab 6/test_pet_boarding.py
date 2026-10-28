import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ============================================================================
# Branch Coverage Tests for boarding_fee()
# ============================================================================

def test_boarding_fee_pet_type_not_in_included_days():
    # Branch 5: True -> unknown pet type raises ValueError
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("iguana", 5, False)


def test_boarding_fee_negative_days():
    # Branch 5: False; Branch 7: True -> negative days raises ValueError
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -3, False)


def test_boarding_fee_premium_rabbit_edge_case():
    # Branch 10: is_premium=True AND pet_type != "rabbit" evaluates to False
    # Verifies rabbit included days remain 4 even with premium kennel
    # Case extra <= 0: days = 4 -> extra = 0 -> fee = 0
    assert boarding_fee("rabbit", 4, True) == 0
    # Case extra > 0: days = 6 -> extra = 2 -> rate = 20 -> fee = 40
    assert boarding_fee("rabbit", 6, True) == 40


def test_boarding_fee_standard_rabbit_regular_stay():
    # Branch 10: is_premium=False AND pet_type != "rabbit" evaluates to False
    # Rabbit standard stay: included = 4, days = 7 -> extra = 3 <= 10, rate = 20 -> fee = 60
    assert boarding_fee("rabbit", 7, False) == 60


def test_boarding_fee_within_included_days_dog():
    # Branch 13: extra <= 0 evaluates to True (days <= included)
    assert boarding_fee("dog", 2, False) == 0
    assert boarding_fee("dog", 1, False) == 0


def test_boarding_fee_dog_standard_under_extra_threshold():
    # Branch 15: pet_type == "dog" -> rate = 30
    # Branch 19: extra <= 10 (False branch) -> days = 7, included = 2, extra = 5 -> fee = 5 * 30 = 150
    assert boarding_fee("dog", 7, False) == 150


def test_boarding_fee_dog_premium_over_extra_threshold():
    # Branch 10: True (is_premium and pet_type != "rabbit") -> included = 2 + 1 = 3
    # Branch 15: pet_type == "dog" -> rate = 30
    # Branch 19: extra > 10 (True branch) -> rate = 30 + 10 = 40
    # Branch 21: pet_type == "dog" (True branch) -> rate = 40 + 5 = 45
    # days = 15 -> extra = 12 -> fee = 12 * 45 = 540
    assert boarding_fee("dog", 15, True) == 540


def test_boarding_fee_cat_standard_under_extra_threshold():
    # Branch 15: pet_type != "dog" -> rate = 20
    # Branch 19: extra <= 10 -> days = 6, included = 3, extra = 3 -> fee = 3 * 20 = 60
    assert boarding_fee("cat", 6, False) == 60


def test_boarding_fee_cat_premium_over_extra_threshold():
    # Branch 10: True (is_premium and pet_type != "rabbit") -> included = 3 + 1 = 4
    # Branch 15: pet_type != "dog" -> rate = 20
    # Branch 19: extra > 10 (True branch) -> rate = 20 + 10 = 30
    # Branch 21: pet_type == "dog" (False branch 21->23) -> rate remains 30
    # days = 16 -> extra = 12 -> fee = 12 * 30 = 360
    assert boarding_fee("cat", 16, True) == 360


def test_boarding_fee_rabbit_over_extra_threshold():
    # Rabbit with extra > 10 to test non-dog extra discount path
    # days = 15, included = 4, extra = 11 > 10 -> rate = 20 + 10 = 30 -> fee = 11 * 30 = 330
    assert boarding_fee("rabbit", 15, False) == 330


# ============================================================================
# Branch Coverage Tests for admission_ok()
# ============================================================================

def test_admission_senior_with_sufficient_vaccinations():
    # Branch 27: is_senior True, vaccinations >= 3 True
    assert admission_ok(11, 3, True) is True
    assert admission_ok(8, 5, True) is True


def test_admission_senior_with_insufficient_vaccinations():
    # Branch 27: is_senior True, vaccinations >= 3 False
    assert admission_ok(10, 2, True) is False
    assert admission_ok(9, 0, True) is False


def test_admission_non_senior_underage():
    # Branch 27: is_senior False; Branch 29: pet_age_years < 1 True
    assert admission_ok(0.8, 4, False) is False
    assert admission_ok(0.0, 3, False) is False


def test_admission_non_senior_adult_sufficient_vaccinations():
    # Branch 27: is_senior False; Branch 29: pet_age_years < 1 False
    # Line 31: vaccinations >= 2 True
    assert admission_ok(1.0, 2, False) is True
    assert admission_ok(4.0, 3, False) is True


def test_admission_non_senior_adult_insufficient_vaccinations():
    # Branch 27: is_senior False; Branch 29: pet_age_years < 1 False
    # Line 31: vaccinations >= 2 False
    assert admission_ok(1.0, 1, False) is False
    assert admission_ok(3.5, 0, False) is False


# ============================================================================
# Branch Coverage Tests for checkout_status()
# ============================================================================

def test_checkout_long_stay_weekend():
    # cutoff = 30 + 20 = 50
    # Open: minutes_left >= 50
    assert checkout_status(55, True, True) == "open"
    assert checkout_status(50, True, True) == "open"
    # Late: 35 <= minutes_left < 50
    assert checkout_status(49, True, True) == "late"
    assert checkout_status(35, True, True) == "late"
    # Closed: minutes_left < 35
    assert checkout_status(34, True, True) == "closed"
    assert checkout_status(0, True, True) == "closed"


def test_checkout_long_stay_weekday():
    # cutoff = 30 + 0 = 30
    # Open: minutes_left >= 30
    assert checkout_status(35, True, False) == "open"
    assert checkout_status(30, True, False) == "open"
    # Late: 15 <= minutes_left < 30
    assert checkout_status(29, True, False) == "late"
    assert checkout_status(15, True, False) == "late"
    # Closed: minutes_left < 15
    assert checkout_status(14, True, False) == "closed"
    assert checkout_status(-1, True, False) == "closed"


def test_checkout_short_stay_weekend():
    # cutoff = 15 + 20 = 35
    # Open: minutes_left >= 35
    assert checkout_status(40, False, True) == "open"
    assert checkout_status(35, False, True) == "open"
    # Late: 20 <= minutes_left < 35
    assert checkout_status(34, False, True) == "late"
    assert checkout_status(20, False, True) == "late"
    # Closed: minutes_left < 20
    assert checkout_status(19, False, True) == "closed"
    assert checkout_status(5, False, True) == "closed"


def test_checkout_short_stay_weekday():
    # cutoff = 15 + 0 = 15
    # Open: minutes_left >= 15
    assert checkout_status(20, False, False) == "open"
    assert checkout_status(15, False, False) == "open"
    # Late: 0 <= minutes_left < 15
    assert checkout_status(14, False, False) == "late"
    assert checkout_status(0, False, False) == "late"
    # Closed: minutes_left < 0
    assert checkout_status(-1, False, False) == "closed"
    assert checkout_status(-10, False, False) == "closed"
