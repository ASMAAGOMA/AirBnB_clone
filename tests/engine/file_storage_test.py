import unittest
import os
from unittest.mock import patch
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorageInstantiation(unittest.TestCase):
    """Test cases for the instantiation of the FileStorage class."""

    def test_file_path_exists(self):
        """Test if the file path exists after instantiation."""
        file_path = FileStorage._FileStorage__file_path
        self.assertTrue(os.path.exists(file_path))

    def test_objects_dict_empty_on_instantiation(self):
        """Test if the __objects dictionary is empty on instantiation."""
        objects_dict = FileStorage._FileStorage__objects
        self.assertDictEqual(objects_dict, {})


class TestFileStorageMethods(unittest.TestCase):
    """Test cases for the methods of the FileStorage class."""

    @patch('models.engine.file_storage.FileStorage.save')
    def test_new_method_adds_object_to_objects_dict(self, mock_save):
        """Test if the new method adds an object to the __objects dictionary."""
        storage = FileStorage()
        obj = BaseModel()
        storage.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, storage._FileStorage__objects)

    @patch('models.engine.file_storage.json.dump')
    def test_save_method_serializes_and_writes_to_file(self, mock_dump):
        """Test if the save method serializes and writes to the file."""
        storage = FileStorage()
        obj = BaseModel()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        storage._FileStorage__objects = {key: obj}
        storage.save()
        mock_dump.assert_called_once()

    @patch('models.engine.file_storage.json.load')
    def test_reload_method_loads_objects_from_file(self, mock_load):
        """Test if the reload method loads objects from the file."""
        storage = FileStorage()
        mock_load.return_value = {
            'BaseModel.123': {'__class__': 'BaseModel', 'id': '123', 'created_at': '2022-01-01T12:00:00.000000', 'updated_at': '2022-01-01T12:00:00.000000'}
        }
        storage.reload()
        self.assertTrue('BaseModel.123' in storage._FileStorage__objects)

    def test_reload_method_handles_file_not_found(self):
        """Test if the reload method handles a FileNotFoundError gracefully."""
        storage = FileStorage()
        with patch('builtins.open', side_effect=FileNotFoundError):
            storage.reload()
        self.assertDictEqual(storage._FileStorage__objects, {})


if __name__ == '__main__':
    unittest.main()
