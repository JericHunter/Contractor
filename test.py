from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_game_id = ObjectId('5d9d0ac88ded608339cde1db')
sample_game = {
    'name': 'Fable',
    'price': '30',
    'img_url': 'https://images-na.ssl-images-amazon.com/images/I/51SGSEAEHKL.jpg'
}
sample_form_data = {
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


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_game(self, mock_find):
        """Test showing a game."""
        mock_find.return_value = sample_game

        result = self.client.get(f'game/{sample_game_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Fable', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_game(self, mock_find):
        """Test editing a game."""
        mock_find.return_value = sample_game

        result = self.client.get(f'edit/{sample_game_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Fable', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_game(self, mock_insert):
        """Test submitting a new game."""
        result = self.client.post('/new-game', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_game)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_game(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/delete/{sample_game_id}', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_game_id})

if __name__ == '__main__':
    unittest_main()
