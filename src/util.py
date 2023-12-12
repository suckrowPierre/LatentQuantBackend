import os
from dotenv import load_dotenv
from currency_converter import CurrencyConverter, ECB_URL

CONVERTER = CurrencyConverter(ECB_URL)

def convert_currency(amount, from_currency, to_currency, date, converter=CONVERTER):
    """
    Convert a given amount from one currency to another.

    :param date: The date of the conversion.
    :param amount: The amount of money to convert.
    :param from_currency: The currency to convert from.
    :param to_currency: The currency to convert to.
    :return: The converted amount.
    """
    if amount == 0 or from_currency == to_currency:
        return amount


    try:
        return converter.convert(amount, from_currency, to_currency, date=date)
    except Exception as e:
        # Handle exceptions such as invalid currency codes
        print(f"Error in currency conversion: {e}")
        # throw error
        raise e


def setup_environment():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()


def get_environment_variable(key):
    """
    Get the value of an environment variable.

    :param key: The key of the environment variable.
    :return: The value of the environment variable.
    """
    try:
        return os.environ[key]
    except KeyError:
        print(f"Error: {key} not found in environment variables")
        # throw error
        raise KeyError
    except Exception as e:
        print(f"Error: {e}")
        # throw error
        raise e


def get_database_currency():
    """
    Get the currency value from the environment variables.

    :return: The database currency.
    """
    return get_environment_variable("DB_CURRENCY")


def get_CSV_path():
    """
    Get the path to the CSV file from the environment variables.

    :return: The path to the CSV file.
    """
    return get_local_path("CSVs_FOLDER")


def get_local_path(env_name):
    """
    Get the path to the local file from the environment variables.

    :return: The path to the local file.
    """
    local_path = get_environment_variable(env_name)
    cwd = os.getcwd()
    path = os.path.join(cwd, local_path)
    return path


def get_hash_path():
    """
    Get the path to the hash file from the environment variables.

    :return: The path to the hash file.
    """
    return get_local_path("HASH_FILE")


def get_hash_algorithm():
    """
    Get the hash algorithm from the environment variables.

    :return: The hash algorithm.
    """
    return get_environment_variable("HASH_ALGORITHM")
