import datetime
import util


def convert_comma_to_point(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None


def get_conversion_datetime(date):
    # return datetime from date with 13:00:00 as time
    return datetime.datetime.combine(date, datetime.time(16, 0, 0))


def convert_string_date_to_date(value):
    try:
        return datetime.datetime.strptime(value, '%d.%m.%Y').date()
    except ValueError:
        return None

#check this online conversion tools seem to differ for the same date
def convert_currency(value, current_currency, target_currency, date, conversion_function=util.convert_currency):
    try:
        return conversion_function(value + 1, current_currency, target_currency, date=get_conversion_datetime(date))
    except ValueError:
        return None


bank_settings = {
    "commerzbank": {
        "dtype": {
            "Umsatzart": str,
            "Buchungstext": str,
            "Währung": str,
            "Auftraggeberkonto": str,
            "Bankleitzahl Auftraggeberkonto": str,
            "IBAN Auftraggeberkonto": str
        },
        "converters": {
            "Buchungstag": convert_string_date_to_date,
            "Wertstellung": convert_string_date_to_date,
            "Betrag": convert_comma_to_point
        },
        "multi-column-converters": {
            "Betrag": (convert_currency, {"value": "Betrag", "current_currency": "Währung", "date": "Buchungstag"}, # commerzbank keine werstellungsdatum für zinsen
                       {"target_currency": "USD"})
        },
        "drop-columns": ["Währung"]

    }

}


def get_bank_settings(institution):
    # make it case-insensitive
    institution = institution.casefold()

    if institution in bank_settings:
        bank_dtype = bank_settings[institution]["dtype"]
        bank_converters = bank_settings[institution]["converters"]
        bank_multi_column_converters = bank_settings[institution]["multi-column-converters"]
        bank_drop_columns = bank_settings[institution]["drop-columns"]

        # Remove dtype for columns that have converters
        for col in bank_converters:
            bank_dtype.pop(col, None)

        return bank_dtype, bank_converters, bank_multi_column_converters, bank_drop_columns

    raise ValueError(f"Bank settings for '{institution}' not found")
