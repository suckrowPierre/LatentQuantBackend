import unittest
from unittest.mock import patch, mock_open
import hashlib
import src.hash as hash
import json
import time

class TestHashFunctions(unittest.TestCase):

    # test get_hash_algorithm()
    def test_get_hash_algorithm(self):
        self.assertEqual(hash.get_hash_algorithm('sha256'), hashlib.sha256)
        self.assertEqual(hash.get_hash_algorithm('sha1'), hashlib.sha1)
        self.assertNotEqual(hash.get_hash_algorithm('sha1'), hashlib.sha256)


    # test hash_file()
    def test_hash_file(self):
        algorithm = hash.get_hash_algorithm('sha256')
        file_path = 'test_hash.py'
        self.assertEqual (hash.hash_file(algorithm, file_path), algorithm(open(file_path, 'rb').read()).hexdigest())
        self.assertNotEqual(hash.hash_file(algorithm, file_path), algorithm(open('test_csv_convert.py', 'rb').read()).hexdigest())

    # test save_hash()
    def test_save_hash_success(self):
        test_hash = "123456789abcdef"
        test_path = "test_path.txt"

        with patch("builtins.open", mock_open()) as mock_file:
            hash.save_hash(test_hash, test_path)
            mock_file.assert_called_with(test_path, 'w')
            mock_file().write.assert_called_once()

    def test_save_hash_no_hash(self):
        test_hash = None
        test_path = "test_path.txt"

        with self.assertRaises(ValueError) as context:
            hash.save_hash(test_hash, test_path)
        self.assertEqual(str(context.exception), "Hash-Value is not defined")

    def test_save_hash_no_file_path(self):
        test_hash = "123456789abcdef"
        test_path = None

        with self.assertRaises(ValueError) as context:
            hash.save_hash(test_hash, test_path)
        self.assertEqual(str(context.exception), "File path is not defined")

    def test_delete_hash_file_success(self):
        test_path = "test_path.txt"

        with patch('os.path.isfile', return_value=True):
            with patch('os.remove') as mock_remove:
                hash.delete_hash_file(test_path)
                mock_remove.assert_called_with(test_path)

    def test_delete_hash_file_no_file_path(self):
        test_path = None

        with self.assertRaises(ValueError) as context:
            hash.delete_hash_file(test_path)
        self.assertEqual(str(context.exception), "File path is not defined")

    def test_delete_hash_file_not_found(self):
        test_path = "non_existent_file.txt"

        with patch('os.path.isfile', return_value=False):
            with self.assertRaises(FileNotFoundError) as context:
                hash.delete_hash_file(test_path)
        self.assertEqual(str(context.exception), "Hash file not found")

    # test load_hashes()

    def test_load_hashes_success(self):
        test_path = "test_path.json"
        test_data = "123456789abcdef"

        with patch('os.path.isfile', return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                result = hash.load_hash_file(test_path)
                self.assertEqual(result, test_data)

    def test_load_hashes_no_file_path(self):
        test_path = None

        with self.assertRaises(ValueError) as context:
            hash.load_hash_file(test_path)
        self.assertEqual(str(context.exception), "File path is not defined")

    def test_load_hashes_invalid_file_path(self):
        test_path = "invalid_path.json"

        with patch('os.path.isfile', return_value=False):
            with self.assertRaises(ValueError) as context:
                hash.load_hash_file(test_path)
        self.assertEqual(str(context.exception), "Hash file path not defined")

    def test_hash_exists_true(self):
        hash_to_check = 'testhash'
        hashes = {'testhash', 'anotherhash'}
        result = hash.hash_exists_single(hash_to_check, hashes)
        self.assertTrue(result)

    def test_hash_exists_false(self):
        hash_to_check = 'nonexistanthash'
        hashes = {'testhash', 'anotherhash'}
        result = hash.hash_exists_single(hash_to_check, hashes)
        self.assertFalse(result)

    def test_hash_exists_no_hash_to_check(self):
        hash_to_check = None
        hashes = {'testhash', 'anotherhash'}
        with self.assertRaises(ValueError) as context:
            hash.hash_exists_single(hash_to_check, hashes)
        self.assertEqual(str(context.exception), "Hash to check is not defined")


    def test_hash_exists_no_hashes(self):
        hash_to_check = 'testhash'
        hashes = None
        with self.assertRaises(ValueError) as context:
            hash.hash_exists_single(hash_to_check, hashes)
        self.assertEqual(str(context.exception), "Hashes are not defined")

    def test_e2e(self):
        hash_algo = 'sha256'
        path = 'hash.json'
        file_to_hash = 'test_hash.py'

        hash_value = hash.hash_file(hash.get_hash_algorithm(hash_algo), file_to_hash)
        hash.save_hash(hash_value, path)
        # delay to make sure file is written
        time.sleep(1)
        read_hash_value = hash.load_hash_file(path)

        # self.assertTrue(hash.hash_exists(hash_value, read_hash_value))
        # hash.delete_hash_file(path)
        # check if file is deleted
        # with self.assertRaises(FileNotFoundError):
            # hash.load_hashes(path)


