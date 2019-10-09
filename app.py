from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import reduce
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()

games_collection = db.games

@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html',games=games_collection.find())

@app.route('/new-game')
def new_game():
    """Return new game creation page."""
    return render_template('new_game.html', title='Game')

@app.route('/new-game', methods=['POST'])
def create_game():
    """Make a new game according to user's specifications."""
    game = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    game_id = games_collection.insert_one(game).inserted_id
    return redirect(url_for('show_game', game_id=game_id))

@app.route('/game/<game_id>')
def show_game(game_id):
    """Show a single game."""
    game = games_collection.find_one({'_id': ObjectId(game_id)})
    return render_template('show_game.html', game=game)

@app.route('/edit/<game_id>', methods=['POST'])
def update_game(game_id):
    """Edit page for a game."""
    new_game = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    games_collection.update_one(
        {'_id': ObjectId(game_id)},
        {'$set': new_game}
    )
    return redirect(url_for('show_game', game_id=game_id))

@app.route('/edit/<game_id>', methods=['GET'])
def edit_game(game_id):
    """Page to submit an edit on a game."""
    game = games_collection.find_one({'_id': ObjectId(game_id)})
    return render_template('edit_game.html', game=game)

@app.route('/delete/<game_id>', methods=['POST'])
def delete_game(game_id):
    """Delete a game."""
    games_collection.delete_one({'_id': ObjectId(game_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
