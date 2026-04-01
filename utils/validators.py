"""Simple validation helpers."""


def validate_range(min_val, max_val):
    if min_val >= max_val:
        raise ValueError("Minimum must be less than maximum")
    return True


def validate_positive(value, name="value"):
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return True


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))
