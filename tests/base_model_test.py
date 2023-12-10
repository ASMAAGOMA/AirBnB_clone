import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from models import BaseModel

class TestBaseModelInstantiation(unittest.TestCase):
    """Test cases for the instantiation of the BaseModel class."""

    @patch('models.storage.new')
    def test_init(self, mock_storage_new):
        """Test case for the instantiation of BaseModel."""
        # Test case when kwargs is empty
        obj = BaseModel()
        self.assertIsNotNone(obj.id)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        mock_storage_new.assert_called_once_with(obj)

        # Test case when kwargs is not empty
        created_at_str = '2022-01-01T12:00:00.000000'
        updated_at_str = '2022-01-02T12:00:00.000000'
        obj = BaseModel(id='123', created_at=created_at_str, updated_at=updated_at_str, custom_attr='value')
        self.assertEqual(obj.id, '123')
        self.assertEqual(obj.custom_attr, 'value')
        self.assertEqual(obj.created_at, datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(obj.updated_at, datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f"))
        mock_storage_new.assert_not_called()

class TestBaseModelSave(unittest.TestCase):
    """Test cases for the save method of the BaseModel class."""

    @patch('models.storage.save')
    def test_save(self, mock_storage_save):
        """Test case for the save method of BaseModel."""
        obj = BaseModel()
        obj.save()
        self.assertIsInstance(obj.updated_at, datetime)
        mock_storage_save.assert_called_once()

    def test_save_updates_updated_at(self):
        """Test case to ensure that calling save updates the updated_at attribute."""
        obj = BaseModel()
        initial_updated_at = obj.updated_at
        obj.save()
        self.assertNotEqual(initial_updated_at, obj.updated_at)

class TestBaseModelToDict(unittest.TestCase):
    """Test cases for the to_dict method of the BaseModel class."""

    def test_to_dict(self):
        """Test case for the to_dict method of BaseModel."""
        created_at_str = '2022-01-01T12:00:00.000000'
        updated_at_str = '2022-01-02T12:00:00.000000'
        obj = BaseModel(id='123', created_at=created_at_str, updated_at=updated_at_str, custom_attr='value')
        obj_dict = obj.to_dict()

        expected_dict = {
            'id': '123',
            'created_at': created_at_str,
            'updated_at': updated_at_str,
            '__class__': 'BaseModel',
            'custom_attr': 'value'
        }

        self.assertEqual(obj_dict, expected_dict)

    def test_to_dict_with_no_custom_attrs(self):
        """Test case for to_dict when there are no custom attributes."""
        obj = BaseModel(id='123', created_at='2022-01-01T12:00:00.000000', updated_at='2022-01-02T12:00:00.000000')
        obj_dict = obj.to_dict()

        expected_dict = {
            'id': '123',
            'created_at': '2022-01-01T12:00:00.000000',
            'updated_at': '2022-01-02T12:00:00.000000',
            '__class__': 'BaseModel',
        }

        self.assertEqual(obj_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
