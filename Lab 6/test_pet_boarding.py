import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# --- Tests for boarding_fee (Code / Statement Coverage) ---

def test_within_included_days():
    # Dog included days = 2, extra <= 0 -> returns 0
    assert boarding_fee("dog", 1, False) == 0
    assert boarding_fee("dog", 2, False) == 0


def test_boarding_fee_invalid_pet():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("parrot", 5, False)


def test_boarding_fee_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("dog", -2, False)


def test_boarding_fee_dog_premium_extra_days():
    # Dog included days = 2 + 1 (premium) = 3; days = 15 -> extra = 12 (> 10)
    # rate = 30 + 10 + 5 = 45; fee = 12 * 45 = 540
    assert boarding_fee("dog", 15, True) == 540


def test_boarding_fee_cat_standard_short_stay():
    # Cat included days = 3; days = 5 -> extra = 2 (<= 10)
    # rate = 20; fee = 2 * 20 = 40
    assert boarding_fee("cat", 5, False) == 40


# --- Tests for admission_ok (Code / Statement Coverage) ---

def test_admission_ok():
    assert admission_ok(4, 2, False) is True


def test_admission_senior_accepted():
    # Senior pet with >= 3 vaccinations
    assert admission_ok(10, 3, True) is True


def test_admission_young_pet_rejected():
    # Non-senior pet with age < 1 year
    assert admission_ok(0.5, 2, False) is False


# --- Tests for checkout_status (Code / Statement Coverage) ---

def test_checkout_long_stay_weekend_open():
    # Long stay (30) + weekend (20) = cutoff 50; minutes_left 50 >= 50 -> "open"
    assert checkout_status(50, True, True) == "open"


def test_checkout_standard_weekday_late():
    # Short stay (15) + weekday (0) = cutoff 15; minutes_left 5 >= 0 -> "late"
    assert checkout_status(5, False, False) == "late"


def test_checkout_standard_weekday_closed():
    # Short stay (15) + weekday (0) = cutoff 15; cutoff - 15 = 0; minutes_left -5 -> "closed"
    assert checkout_status(-5, False, False) == "closed"
