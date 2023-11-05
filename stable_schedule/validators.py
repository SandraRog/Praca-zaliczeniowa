from django.core.exceptions import ValidationError


def check_amount(value):
    if value > 50:
        raise ValidationError("Unfortunately, horses don`t live that long...")
    elif value < 0:
        raise ValidationError("Your horse hasn't been born yet'")