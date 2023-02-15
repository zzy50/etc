import re

def is_valid_format_date(_date) :
    # regex = r'\d{6}'
    # regex = r'\d{6}_\d{6}'
    regex = r'date_\d{6}'
    return  bool(re.match(regex, _date))

_date = "date_155521"
print(is_valid_format_date(_date))