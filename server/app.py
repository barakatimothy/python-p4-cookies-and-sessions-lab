#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False  # Fix: It should be app.json_encoder.compact

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

from flask import request

@app.route('/articles', methods=['GET'])
def get_all_articles():
    # Get all articles from the database
    articles = Article.query.all()

    # Check if there are any articles
    if articles:
        # Create a list to store article data
        articles_data = []

        # Iterate through each article and add its data to the list
        for article in articles:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                # Add other fields as needed
            })

        # Return JSON response with the list of articles
        return jsonify({'articles': articles_data}), 200
    else:
        # Return a JSON response indicating that no articles were found
        return jsonify({'message': 'No articles found'}), 404


@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Set the initial value to 0 if it's the first request for this user
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for every request
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        # Get the article data (you need to implement this)
        article = Article.query.get(id)
        if article:
            # Render JSON response with article data
            return jsonify({
                'message': f'Successfully viewed article {id}',
                'article': {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content
                    # Add other fields as needed
                }
            }), 200
        else:
            # Handle the case where the article with the given id is not found
            return {'message': '404: Article not found'}, 404
    else:
        # Render JSON response with an error message for exceeding the pageview limit
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
