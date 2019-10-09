from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

class GameTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""
        # Get the Flask test client
        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the OGXB homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Game', result.data)

    def test_new(self):
        """Test the new game creation page."""
        result = self.client.get('/new-game')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Game', result.data)

if __name__ == '__main__':
    unittest_main()
