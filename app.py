import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import Game, Review, setup_db
from auth import AuthError, requires_auth

GAMES_PER_PAGE = 8

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
      response.headers.add('Access-Control-Allow-Headers', "GET,POST,PATCH,DELETE")
      return response

#----------------------------------------------------------------------------#
# Helper functions
#----------------------------------------------------------------------------#
  def format_games(request, gamesList):
      games = [game.format() for game in gamesList]
      return games

#----------------------------------------------------------------------------#
# API Endpoints
#----------------------------------------------------------------------------#
    # get_games will return a list of games and the # of reviews for each games
    # as well as a average rating for each game (given a review is present).

  @app.route('/games', methods=['GET'])
  @requires_auth('get:items')
  def get_games(payload):
      try:
        DBGames = Game.query.all()
        formattedGames = format_games(request, DBGames)
        if len(formattedGames) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'games': formattedGames
        })
      except:
        abort(404)

  @app.route('/review/<int:game_id>', methods=['GET'])
  @requires_auth('get:items')
  def get_reviews(payload, game_id):
      try:
        DBreview = Review.query.filter(Review.game_id == game_id).all()
        if len(DBreview) > 0:
            returnReviews = [review.format() for review in DBreview]
            return jsonify({
                'success': True,
                'reviews': returnReviews
                })
        else:
            abort(404)
      except:
          abort(404)


  @app.route('/games', methods=['POST'])
  @requires_auth('add:items')
  def add_game(payload):
      body = request.get_json()
      title = body['title']
      type = body['type']
      genre = body['genre']
      category = body['category']
      description = body['description']
      #Check that non-nullable fields have something in them
      if len(title) > 0 and len(genre) > 0:
          newGame = Game(title, type, genre, category, description)
          newGame.insert()
          return jsonify({
              'success': True
          })
      else:
          abort(422)

  @app.route('/review', methods=['POST'])
  @requires_auth('add:items')
  def add_review(payload):
      body = request.get_json()
      game_id = body['game_id']
      rating = body['rating']
      reviewer = body['reviewer']
      review = body['review']
      #Check database to make sure game exists in database
      try:
          DBGame = Game.query.filter(Game.id == game_id).first()
          newReview = Review(game_id, rating, reviewer, review)
          newReview.insert()
          return jsonify({
            'success': True
            })
      except:
          abort(404)


  @app.route('/games/<int:game_id>', methods=['DELETE'])
  @requires_auth('edit:items')
  def delete_game(payload, game_id):
      try:
          DBGame = Game.query.filter(Game.id == game_id).first()
          DBGame.delete()
          return jsonify({
              'success': True
          })
      except:
          abort(404);

  @app.route('/review/<int:review_id>', methods=['DELETE'])
  @requires_auth('edit:items')
  def delete_review(payload, review_id):
      try:
          DBReview = Review.query.filter(Review.id == review_id).first()
          DBReview.delete()
          return jsonify({
              'success': True
          })
      except:
          abort(404)

  @app.route('/games/<int:game_id>', methods=['PATCH'])
  @requires_auth('edit:items')
  def patch_game(payload, game_id):
      try:
          body = request.get_json()
          DBGame = Game.query.filter(Game.id == game_id).first()
          if 'title' in body:
              DBGame.title = body['title']
          if 'type' in body:
              DBGame.type = body['type']
          if 'genre' in body:
              DBGame.genre = body['genre']
          if 'category' in body:
              DBGame.category = body['category']
          if 'description' in body:
              DBGame.description = body['description']
          DBGame.update()
          return jsonify({
              'success': True
          })
      except:
          abort(404)

  @app.route('/review/<int:review_id>', methods=['PATCH'])
  @requires_auth('edit:items')
  def patch_review(payload, review_id):
      try:
          body = request.get_json()
          DBReview = Review.query.filter(Review.id == review_id).first()
          if 'rating' in body:
              DBReview.rating = body['rating']
          if 'reviewer' in body:
              DBReview.reviewer = body['reviewer']
          if 'review' in body:
              DBReview.review = body['review']
          DBReview.update()
          return jsonify({
              'success': True,
              'review': DBReview.format()
          })
      except:
          abort(404)

#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#

  @app.errorhandler(404)
  def not_found_error(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'Requested resource not found.'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Request was not processable.'
      }), 422

  @app.errorhandler(AuthError)
  def handle_auth_error(error):
      return jsonify({
        'success': False,
        'message': 'Authentication Error',
        'authentication_error_message': error.error,
        'error': error.status_code
    }), error.status_code

  return app

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
