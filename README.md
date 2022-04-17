# FNSD

## Casting Agency Protected API

The application demonstrates create, read, update, delete APIs for Movies and Actors and also demonstrates Many to Many relationship for Movies Casts having multiple

## Tasks

1. Setup Authentication
2. Deploy application in Heroku.

### 1. Setup Authentication

For Authentication and authorization we use Auth0. Following steps need to be performed:
1. Create an account in Auth0, you get a default tenant.
2. Create API and name it casting-agency
3. Add Permissions in the API 
   - read:actors
   - add:actor
   - edit:actor
   - delete:actor
   - read:movies
   - add:movie
   - edit:movie
   - delete:movie
4. Create an application for testing which will give you Client ID and Client Sectret.
4.1 Enable grant type password in advanced setting for the test application.
5. Create 3 roles and assign appropriate permissions
   - Casting Assistant (read:actors, read:movies)
   - Casting Director (add:actor, delete:actor, edit:actor, edit:movie, read:actors, read:movies)
   - Executive Producer (add:actor, delete:actor, edit:actor, edit:movie, read:actors, read:movies, add:movie, delete:movie)
5. Under User Management > Users, create three users:
   - casting_assistant@castingagency.com and assign role Casting Assistant
   - casting_director@castingagency.com and assign role Casting Director
   - executive_produceer@castingagency.com and assign role Executive Producer
6. Configure app.py to support authentication and authorization

AUTH0_DOMAIN = '<domain from auth0>'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-agency'


eg
```
@app.route('/api/v1/actors', methods=['POST'])
    @requires_auth
    def create_actor(payload):
        if requires_scope("add:actor"):
            data = request.get_json()
            print(data)
            actor = Actor(first_name=data['firstName'], last_name=data['lastName'], gender=data['gender'], date_of_birth=data['dateOfBirth'], age = data['age'])
            actor.create()
            return make_response(jsonify({"result": "Actor created successfuly."}), 200)
        raise AuthError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
```


### 2. Deploy application in Heroku.

To run the application locally:
1. python -m pip install -r requirements.tx
2. python -m flask run

Application should start on http://localhos:5000/

To run the application on Heroku.
1. Get an account on Heroku.
2. In project directory, do following steps
2.1 git init
2.2 heroku login
3.3 git commit -m "Commit code"
3.4 git push heroku master

The application should be available on https://<app name>.herokuapp.com
eg: fsnd-heroku-app.herokuapp.com






