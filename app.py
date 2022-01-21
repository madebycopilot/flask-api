# Import flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# import Flask SQLALchemy
from flask_sqlalchemy import SQLAlchemy

# Create a flask app
app = Flask(__name__)

# Create app configuration for SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# Connect app to SQLAlchemy database
db = SQLAlchemy(app)

# Create an SQLAlchemy model for Users
class User(db.Model):
    # Create a table in the database
    __tablename__ = 'users'
    # Create columns for the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# If tables do not exist, create them
try:
    db.create_all()
except:
    pass

# Create an index route and return a JSON response
@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

# Create an API route for the model User with post, get, put and delete methods
@app.route('/users', methods=['GET', 'POST'])
def users():
    # Create a variable to store the users data
    users_data = []
    # If the request method is POST, add data to the database
    if request.method == 'POST':
        # Create variables to store the data from the request
        username = request.json.get('username')
        email = request.json.get('email')
        # Create a new user with the data from the request
        new_user = User(username=username, email=email)
        # Add the new user to the database
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        # Add the new user's data to the users_data variable
        users_data.append({'username': new_user.username, 'email': new_user.email})
    # If the request method is GET, get all of the users data from the database
    elif request.method == 'GET':
        # Get all of the users from the database
        users = User.query.all()
        # Iterate over all of the users
        for user in users:
            # Add the user's data to the users_data variable
            users_data.append({'username': user.username, 'email': user.email})
    # Return the users_data variable as a JSON response
    return jsonify(users_data)

# Create an API route for the model User to return a single user based on the id
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user(id):
    # Create a variable to store the user data
    user_data = []
    # If the request method is GET, get the user's data from the database
    if request.method == 'GET':
        # Get the user from the database
        user = User.query.get(id)
        # Add the user's data to the user_data variable
        user_data.append({'username': user.username, 'email': user.email})
    # If the request method is PUT, update the user's data in the database
    elif request.method == 'PUT':
        # Get the user from the database
        user = User.query.get(id)
        # Update the user's data with the data from the request
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        # Add the user's data to the user_data variable
        user_data.append({'username': user.username, 'email': user.email})
        # Commit the changes to the database
        db.session.commit()
    # If the request method is DELETE, delete the user from the database
    elif request.method == 'DELETE':
        # Get the user from the database
        user = User.query.get(id)
        # Delete the user from the database
        db.session.delete(user)
        # Commit the changes to the database
        db.session.commit()
    # Return the user_data variable as a JSON response
    return jsonify(user_data)

# Write a function that runs the flask app
if __name__ == '__main__':
    app.run(debug=True)
