from django import template
from membership.nepali_date import NepaliDate

register = template.Library()


@register.filter(name='nepali')
def nepali_date(value, format_type='short'):
    """
    Convert AD date to Nepali date
    
    Usage in templates:
        {{ member.date_of_birth|nepali }}  → 2081-03-15
        {{ member.date_of_birth|nepali:"medium" }}  → 15 Ashadh 2081
        {{ member.date_of_birth|nepali:"long" }}  → 15 Ashadh, 2081
    """
    if not value:
        return ""
    return NepaliDate.format_nepali_date(value, format_type)


@register.filter(name='dual_date')
def dual_date(value, date_format='short'):
    """
    Display both AD and BS dates
    
    Usage in templates:
        {{ member.date_of_birth|dual_date }}  → 2024-06-28 (2081-03-15 BS)
        {{ member.date_of_birth|dual_date:"medium" }}  → Jun 28, 2024 (15 Ashadh 2081 BS)
    """
    if not value:
        return ""
    
    from django.utils.dateformat import format as date_format_func
    
    # Format AD date
    if date_format == 'short':
        ad_str = value.strftime('%Y-%m-%d')
        bs_str = NepaliDate.format_nepali_date(value, 'short')
    else:  # medium/long
        ad_str = value.strftime('%b %d, %Y')
        bs_str = NepaliDate.format_nepali_date(value, 'medium')
    
    # Return combined
    if bs_str:
        return f"{ad_str} ({bs_str} BS)"
    return ad_str


@register.filter(name='abs')
def absolute_value(value):
    """
    Return the absolute value of a number
    
    Usage in templates:
        {{ number|abs }}  → Returns absolute value
        Example: {{ -5|abs }} → 5
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value


@register.filter(name='format_number')
def format_number(value):
    """
    Format number with commas as thousands separator
    
    Usage in templates:
        {{ 1000000|format_number }}  → 1,000,000
        {{ 5000.50|format_number }}  → 5,000.50
    """
    try:
        # Convert to float first to handle both int and float
        num = float(value)
        # Format with commas
        if num == int(num):
            # If it's a whole number, show no decimals
            return "{:,}".format(int(num))
        else:
            # If it has decimals, show 2 decimal places
            return "{:,.2f}".format(num)
    except (ValueError, TypeError):
        return value


@register.filter(name='format_currency')
def format_currency(value):
    """
    Format currency with NPR prefix and commas
    
    Usage in templates:
        {{ 1000000|format_currency }}  → NPR 1,000,000
        {{ 5000.50|format_currency }}  → NPR 5,000.50
    """
    try:
        num = float(value)
        if num == int(num):
            return "NPR {:,}".format(int(num))
        else:
            return "NPR {:,.2f}".format(num)
    except (ValueError, TypeError):
        return value


@register.filter(name='format_amount')
def format_amount(value):
    """
    Format amount with 2 decimal places and commas
    
    Usage in templates:
        {{ 1000.5|format_amount }}  → 1,000.50
        {{ 1000|format_amount }}  → 1,000.00
    """
    try:
        num = float(value)
        return "{:,.2f}".format(num)
    except (ValueError, TypeError):
        return value