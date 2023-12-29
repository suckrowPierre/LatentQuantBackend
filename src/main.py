import util
import hash
import csv_convert
import pandas as pd
import bank_data_processors as bank_processors
from currency_converter import CurrencyConverter, ECB_URL

util.setup_environment()
CURRENCY = util.get_database_currency()
HASH_ALGORITHM = hash.get_hash_algorithm(util.get_hash_algorithm())
HASH_PATH = util.get_hash_path()
CSV_FILE_PATH = util.get_CSV_path()
BANK_ACCOUNT_DETAILS_PATH = util.get_bank_account_details_path()






def get_csv_dicts_with_hash(csv_file_names):
    """
    Get the CSV files as dictionaries with the hash value.

    With the format
    {
        "path": path_to_csv,
        "hash": hash_value,
    }
    :param csv_file_names:
    :return csv_dicts:
    """

    csv_dicts = []
    for csv_file_name in csv_file_names:
        csv_dicts.append({
            "path": csv_file_name,
            "hash": hash.hash_file(HASH_ALGORITHM, csv_file_name)
        })
    return csv_dicts


def filter_existing_hashes(hash_file_dict):
    """
    Filter out hashes that already exist.

    :return: A list of hashes that do not exist.
    """
    if not hash_file_dict:
        print("Error: Hashes to check are not defined")
        # throw error
        raise ValueError("Hashes to check are not defined")
    try:
        hashes = hash.load_hash_file(HASH_PATH)
    except FileNotFoundError:
        print("Warning: Hash file not found")
        return hash_file_dict

    return [dict_entry for dict_entry in hash_file_dict if not hash.hash_exists_single(dict_entry["hash"], hashes)]


def main():
    csv_dicts = filter_existing_hashes(
        get_csv_dicts_with_hash(csv_convert.load_csvs_file_names(CSV_FILE_PATH, full_path=True)))

    print(csv_dicts)

    bank_details = bank_processors.getBankDetails(BANK_ACCOUNT_DETAILS_PATH)
    print(bank_details)

    # data = csv_convert.panda_read_csv(csv_dicts[0]["path"])


if __name__ == "__main__":
    main()
