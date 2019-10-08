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
    return render_template('new_game.html')

@app.route('/new-game', methods=['POST'])
def create_candy():
    """Make a new game according to user's specifications."""
    game = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    game_id = game_collection.insert_one(game).inserted_id
    return redirect(url_for('show_game', game_id=game_id))


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
