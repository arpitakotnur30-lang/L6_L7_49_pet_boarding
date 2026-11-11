import math

def parse_booking(text):
    """
    Parses a booking string in the format 'pet:days'.
    Hardened against: None, non-strings, missing/extra delimiters, 
    empty strings, invalid numbers, negative days, NaN/Inf.
    Returns: (pet_name_title_cased, days_as_float) or None on invalid input.
    """
    if not isinstance(text, str):
        return None
    
    parts = text.split(':')
    if len(parts) != 2:
        return None
    
    pet = parts[0].strip()
    days_str = parts[1].strip()
    
    if not pet:
        return None
    
    try:
        days = float(days_str)
        if math.isnan(days) or math.isinf(days) or days < 0:
            return None
        return pet.title(), days
    except (ValueError, TypeError, OverflowError):
        return None

def stay_average(days_csv):
    """
    Computes integer average of stay lengths from comma-separated days.
    Hardened against: None, non-strings, empty strings, missing values, non-integers,
    division by zero, negative days, and overflow.
    Returns: integer average or 0 on empty/invalid input.
    """
    if not isinstance(days_csv, str):
        return 0
    
    raw_tokens = days_csv.split(',')
    values = []
    for r in raw_tokens:
        token = r.strip()
        if not token:
            continue
        try:
            val = int(token)
            if val < 0:
                return 0
            values.append(val)
        except (ValueError, TypeError, OverflowError):
            return 0
    
    if not values:
        return 0
    return sum(values) // len(values)

def payable_fee(text):
    """
    Calculates payable fee after discount and 18% tax from 'fee|discount'.
    Hardened against: None, non-strings, missing/extra delimiters, non-numeric values,
    NaN, Inf, negative fees/discounts, and overflow.
    Returns: payable fee (float >= 0.0) or 0.0 on invalid input.
    """
    if not isinstance(text, str):
        return 0.0
    
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    
    try:
        fee = float(parts[0].strip())
        discount = float(parts[1].strip())
        if math.isnan(fee) or math.isinf(fee) or math.isnan(discount) or math.isinf(discount):
            return 0.0
        if fee < 0 or discount < 0:
            return 0.0
        total = fee * 1.18 - discount
        return max(total, 0.0)
    except (ValueError, TypeError, OverflowError):
        return 0.0

def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)

if __name__ == "__main__":
    main()