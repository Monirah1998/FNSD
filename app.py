import os
from flask import Flask, request, abort, make_response, jsonify
from models import setup_db, Actor, Movie
from flask_cors import CORS
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-i2ernxx1.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://dev-i2ernxx1.us.auth0.com/api/v2/'

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    @requires_auth
    def get_greeting(payload):
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    @app.route('/api/v1/person', methods=['POST'])
    def create_person():
        data = request.get_json()
        print(data)
        person = Person(name=data['name'], catchphrase=data['catchphrase'])
        person.create()
        return make_response(jsonify({"todo": ""}), 200)

    @app.route('/api/v1/actors', methods=['POST'])
    def create_actor():
        data = request.get_json()
        print(data)
        actor = Actor(first_name=data['firstName'], last_name=data['lastName'], gender=data['gender'], date_of_birth=data['dateOfBirth'], age = data['age'])
        actor.create()
        return make_response(jsonify({"result": "Actor created successfuly."}), 200)
    
    @app.route('/api/v1/actors', methods=["GET"])
    def get_all_actors():
        actors = Actor.query.all()
        if actors is None:
            abort(404)
        return make_response(jsonify({
        "actors": [actor.format() for actor in actors]
        }), 200)
    
    @app.route('/api/v1/actors/<int:id>', methods=["GET"])
    def get_actor(id):
        actor=Actor.query.get(id)
        if actor is None:
            abort(404)
        return make_response(jsonify(actor.format()),200)
    
    @app.route('/api/v1/actors/<int:id>', methods=["PATCH"])
    def update_actor(id):
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

    @app.route('/api/v1/actors/<int:id>', methods=["DELETE"])
    def delete_actor(id):
        actor=Actor.query.get(id)
        if actor is None:
            abort(404)
        actor.delete()
        return make_response(jsonify({"result": "Actor deleted successfuly."}), 200)

    '''
    Movies Controllers
    '''
    @app.route('/api/v1/movies', methods=['POST'])
    def create_movie():
        data = request.get_json()
        print(data)
        movie = Movie(title=data['title'], genre=data['genre'], rating=data['rating'], release_date=data['releaseDate'])
        movie.create()
        return make_response(jsonify({"result": "Movie created successfuly."}), 200)
    
    @app.route('/api/v1/movies', methods=["GET"])
    def get_all_movies():
        movies = Movie.query.all()
        if movies is None:
            abort(404)
        return make_response(jsonify({
        "actors": [movie.format() for movie in movies]
        }), 200)
    
    @app.route('/api/v1/movies/<int:id>', methods=["GET"])
    def get_movie(id):
        movie=Movie.query.get(id)
        print(movie.cast)
        for actor in movie.cast:
            print(actor.first_name)
        if movie is None:
            abort(404)
        return make_response(jsonify(movie.format()),200)
    
    @app.route('/api/v1/movies/<int:id>', methods=["PATCH"])
    def update_movie(id):
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

    @app.route('/api/v1/movies/<int:id>', methods=["DELETE"])
    def delete_movie(id):
        movie=Movie.query.get(id)
        if movie is None:
            abort(404)
        movie.delete()
        return make_response(jsonify({"result": "Movie deleted successfuly."}), 200)

    @app.route('/api/v1/movies/<int:movieid>/actor/<int:actorid>', methods=['POST'])
    def create_movie_cast(movieid,actorid):
        movie=Movie.query.get(movieid)
        actor=Actor.query.get(actorid)
        movie.cast.append(actor)
        movie.update()
        return make_response(jsonify({"result": "Movie cast created successfuly."}), 200)

    return app

class AuthError(Exception):
        def __init__(self, error, status_code):
            self.error = error
            self.status_code = status_code

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token_auth_header()
        print("Token="+token)
        try:
            payload = verify_decode_jwt(token)
        except Exception as ex:
            print(ex)
            abort(401)
        return f(payload, *args, **kwargs)
    return wrapper

app = create_app()

if __name__ == '__main__':
    app.run()
