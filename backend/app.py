"""Flask application entry point."""

from flask import Flask, jsonify
from flask_cors import CORS
from backend.routes.api import api
from backend.config.database import init_db, init_default_tickers
import os


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False

    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(api)

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Stock & Crypto News Sentiment API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'tickers': '/api/tickers',
                'articles': '/api/articles',
                'sentiment_summary': '/api/sentiment/summary',
                'process': '/api/process',
                'ticker_latest': '/api/ticker/<ticker>/latest'
            }
        })

    return app


if __name__ == '__main__':
    # Initialize database
    init_db()
    init_default_tickers()

    # Create and run app
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
