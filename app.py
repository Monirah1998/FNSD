import os
from flask import Flask, request, abort, make_response, jsonify
from models import setup_db, Actor, Movie
from flask_cors import CORS
import json

from auth import requires_authentication, requires_permission, AuthenticationError





def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/api/v1/actors', methods=['POST'])
    @requires_authentication
    def create_actor(payload):
        if requires_permission("add:actor"):
            data = request.get_json()
            actor = Actor(first_name=data['firstName'], last_name=data['lastName'], gender=data['gender'], date_of_birth=data['dateOfBirth'], age = data['age'])
            actor.create()
            return make_response(jsonify({"result": "Actor created successfuly."}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/actors', methods=["GET"])
    @requires_authentication
    def get_all_actors(payload):
        if requires_permission("read:actors"):
            actors = Actor.query.all()
            if actors is None:
                abort(404)
            return make_response(jsonify({
            "actors": [actor.format() for actor in actors]
            }), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/actors/<int:id>', methods=["GET"])
    @requires_authentication
    def get_actor(payload, id):
        if requires_permission("read:actors"):
            actor=Actor.query.get(id)
            if actor is None:
                abort(404)
            return make_response(jsonify(actor.format()),200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/actors/<int:id>', methods=["PATCH"])
    @requires_authentication
    def update_actor(payload, id):
        if requires_permission("edit:actor"):
            data = request.get_json()
            actor=Actor.query.get(id)
            if actor is None:
                abort(404)
            
            if 'firstName' in data:
                actor.first_name = data['firstName']
            
            if 'lastName' in data:
                actor.last_name = data['lastName']

            if 'gender' in data:
                actor.gender = data['gender']

            if 'age' in data:
                actor.age = data['age']

            if 'dateOfBirth' in data:
                actor.date_of_birth = data['dateOfBirth']
            actor.update()
            actor = Actor.query.get(id)
            return make_response(jsonify({"result": "Actor updated successfuly.", "actor": actor.format()}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)

    @app.route('/api/v1/actors/<int:id>', methods=["DELETE"])
    @requires_authentication
    def delete_actor(payload, id):
        if requires_permission("delete:actor"):
            actor=Actor.query.get(id)
            if actor is None:
                abort(404)
            actor.delete()
            return make_response(jsonify({"result": "Actor deleted successfuly."}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)

    '''
    Movies Controllers
    '''
    @app.route('/api/v1/movies', methods=['POST'])
    @requires_authentication
    def create_movie(payload):
        if requires_permission("add:movie"):
            data = request.get_json()
            movie = Movie(title=data['title'], genre=data['genre'], rating=data['rating'], release_date=data['releaseDate'])
            movie.create()
            return make_response(jsonify({"result": "Movie created successfuly."}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/movies', methods=["GET"])
    @requires_authentication
    def get_all_movies(payload):
        if requires_permission("read:movies"):
            movies = Movie.query.all()
            if movies is None:
                abort(404)
            return make_response(jsonify({
            "movies": [movie.format() for movie in movies]
            }), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/movies/<int:id>', methods=["GET"])
    @requires_authentication
    def get_movie(payload, id):
        if requires_permission("read:movies"):
            movie=Movie.query.get(id)
            if movie is None:
                abort(404)
            return make_response(jsonify(movie.format()),200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
    
    @app.route('/api/v1/movies/<int:id>', methods=["PATCH"])
    @requires_authentication
    def update_movie(payload, id):
        if requires_permission("edit:movie"):
            data = request.get_json()
            movie=Movie.query.get(id)
            if movie is None:
                abort(404)
            
            if 'title' in data:
                movie.title = data['title']
            
            if 'genre' in data:
                movie.genre = data['genre']

            if 'rating' in data:
                movie.rating = data['rating']

            if 'releaseDate' in data:
                movie.release_date = data['releaseDate']
            movie.update()
            movie = Movie.query.get(id)
            return make_response(jsonify({"result": "Movie updated successfuly.", "movie": movie.format()}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)

    @app.route('/api/v1/movies/<int:id>', methods=["DELETE"])
    @requires_authentication
    def delete_movie(payload, id):
        if requires_permission("delete:movie"):
            movie=Movie.query.get(id)
            if movie is None:
                abort(404)
            movie.delete()
            return make_response(jsonify({"result": "Movie deleted successfuly."}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)

    @app.route('/api/v1/movies/<int:movieid>/actor/<int:actorid>', methods=['POST'])
    @requires_authentication
    def create_movie_cast(payload, movieid,actorid):
        if requires_permission("edit:movie"):
            movie=Movie.query.get(movieid)
            actor=Actor.query.get(actorid)
            movie.cast.append(actor)
            movie.update()
            return make_response(jsonify({"result": "Movie cast created successfuly."}), 200)
        raise AuthenticationError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)

    @app.errorhandler(AuthenticationError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app







app = create_app()

if __name__ == '__main__':
    app.run()
