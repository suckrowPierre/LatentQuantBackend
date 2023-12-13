import os
import pandas as pd
import bank_data_processors as bank_dict


def load_csvs_file_names(folder_path, full_path=False):
    """
    Load all CSV file names from a folder.

    :param full_path:
    :param folder_path: The path to the folder.
    :return: A list of CSV file names.
    :raises ValueError: If the folder path is not defined or not a valid directory.
    """
    if not folder_path:
        raise ValueError("Folder path is not defined")

    if not os.path.isdir(folder_path):
        raise ValueError("Folder path is not valid")

    def condition(file):
        return file.endswith('.csv') or file.endswith('.CSV')

    if full_path:
        return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if condition(file)]
    else:
        return [file for file in os.listdir(folder_path) if condition(file)]


def panda_read_csv(file_path):
    """
    Read a CSV file as pandas DataFrame.

    :param file_path: The path to the CSV file.
    :return: The CSV file as pandas DataFrame.
    """
    if not file_path:
        raise ValueError("File path is not defined")

    if not os.path.isfile(file_path):
        raise ValueError("File path is not valid")

    bank_name = "commerzbank"  # This can be made dynamic based on the file or input
    bank_dtype, bank_converters, bank_multi_column_converters, bank_drop_columns = bank_dict.get_bank_settings(bank_name)

    try:
        data = pd.read_csv(file_path, sep=';', dtype=bank_dtype, converters=bank_converters)

        print(data.to_markdown())
        # multi-column converters
        for column, (converter, column_mapping, static_args) in bank_multi_column_converters.items():
            # Construct the arguments for each row
            def apply_converter(row):
                converter_args = {arg_name: row[column_name] for arg_name, column_name in column_mapping.items()}
                return converter(**converter_args, **static_args)

            data[column] = data.apply(apply_converter, axis=1)

        data.drop(columns=bank_drop_columns, inplace=True, errors='ignore')

        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        print(data.to_markdown())



        # drop columns
        return data
    except Exception as e:
        raise e
