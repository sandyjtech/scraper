from flask import Flask, jsonify
from flask_restful import Api, Resource
import requests
import logging

app = Flask(__name__)
api = Api(app)

# Define your WordPress API endpoint and authentication details
WORDPRESS_API_URL = 'https://balancedcomfort.com/wp-json/wp/v2'
USERNAME = 'SandraG'
PASSWORD = ''  # Replace with your actual password

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to authenticate and get JWT token
def get_auth_token(username, password):
    auth_url = 'https://balancedcomfort.com/wp-json/jwt-auth/v1/token'
    try:
        response = requests.post(auth_url, json={
            'username': username,
            'password': password
        })
        response.raise_for_status()  # Raise an HTTPError for bad status codes
        return response.json().get('token')
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to authenticate: {e}")
        return None

# Function to fetch WordPress posts
def get_wordpress_posts(token):
    posts_url = f'{WORDPRESS_API_URL}/posts'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(posts_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch posts: {e}")
        return None

# Flask-RESTful API endpoint to fetch WordPress posts
class WordpressPage(Resource):
    def get(self):
        token = get_auth_token(USERNAME, PASSWORD)
        if token:
            posts = get_wordpress_posts(token)
            if posts is not None:
                return jsonify(posts), 200
            else:
                return {'error': 'Failed to fetch posts'}, 500
        else:
            return {'error': 'Failed to authenticate'}, 401