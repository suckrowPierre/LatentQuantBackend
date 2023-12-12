import hashlib
import json
import os

def get_hash_algorithm(algorithm_name):
    """
    Get the hash algorithm from the environment variables.

    :return: The hash algorithm.
    """
    if not algorithm_name:
        print("Error: Hash algorithm is not defined")
        # throw error
        raise ValueError("Hash algorithm is not defined")

    if algorithm_name not in hashlib.algorithms_available:
        print(f"Error: {algorithm_name} is not a valid hash algorithm")
        # throw error
        raise ValueError

    return getattr(hashlib, algorithm_name)

def hash_file(algorithm, file_path):
    """
    Hash a file.

    :param algorithm: The hash algorithm.
    :param file_path: The path to the file.
    :return: The hash of the file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a file")
        # throw error
        raise FileNotFoundError("Hash file not found")
    # check if algorithm is defined
    if not algorithm:
        print("Error: Hash algorithm is not defined")
        # throw error
        raise ValueError("Hash algorithm is not defined")

    with open(file_path, 'rb') as file:
        return algorithm(file.read()).hexdigest()

def save_hash(hash, file_path):
    """
    Save a hash to a file.

    :param hash: The hash.
    :param file_path: The path to the file.
    """
    if not hash:
        print("Error: Hash-Value is not defined")
        # throw error
        raise ValueError("Hash-Value is not defined")
    if not file_path:
        print("Error: File path is not defined")
        # throw error
        raise ValueError("File path is not defined")

    with open(file_path, 'w') as file:
        json.dump(hash, file)

def delete_hash_file(file_path):
    """
    Delete the hash file.
    """
    if not file_path:
        print("Error: File path is not defined")
        # throw error
        raise ValueError("File path is not defined")

    if not os.path.isfile(file_path):
        print("Error: Hash file not found")
        # throw error
        raise FileNotFoundError("Hash file not found")

    os.remove(file_path)

def load_hash_file(file_path):
    """
    Load hashes from json file.

    :param file_path: The path to the file.
    :return: The hash.
    """
    if not file_path:
        print("Error: File path is not defined")
        # throw error
        raise ValueError("File path is not defined")

    if not os.path.isfile(file_path):
        print("Error: Hash file not found")
        # throw error
        raise FileNotFoundError("Hash file not found")

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: Hash file not found")
        raise FileNotFoundError
    except Exception as e:
        raise e

def hash_exists_single(hash_to_check, hashes):
    """
    Check if a hash exists.

    :return: True if the hash exists, False otherwise.
    """
    if not hash_to_check:
        print("Error: Hash to check is not defined")
        # throw error
        raise ValueError("Hash to check is not defined")
    if not hashes:
        print("Error: Hashes are not defined")
        # throw error
        raise ValueError("Hashes are not defined")

    return hash_to_check in hashes



