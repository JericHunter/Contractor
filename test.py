from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_game_id = ObjectId('5d9d0ac88ded608339cde1db')
sample_game = {
    'name': 'Fable',
    'price': '30',
    'img_url': 'https://images-na.ssl-images-amazon.com/images/I/51SGSEAEHKL.jpg'
}
sample_game_data = {
    'name': sample_game['name'],
    'price': sample_game['price'],
    'img_url': sample_game['img_url']
}

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
