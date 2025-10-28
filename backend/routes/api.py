"""Flask API routes for the news sentiment application."""

from flask import Blueprint, jsonify, request
from backend.models.news_article import NewsArticle, TickerConfig
from backend.config.database import SessionLocal
from backend.services.pipeline import NewsPipeline
from sqlalchemy import desc, func
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


@api.route('/tickers', methods=['GET'])
def get_tickers():
    """Get all ticker configurations."""
    db = SessionLocal()
    try:
        tickers = db.query(TickerConfig).all()
        return jsonify([ticker.to_dict() for ticker in tickers])
    finally:
        db.close()


@api.route('/tickers', methods=['POST'])
def add_ticker():
    """Add a new ticker to monitor."""
    data = request.json
    db = SessionLocal()

    try:
        ticker = TickerConfig(
            ticker=data['ticker'].upper(),
            name=data.get('name', ''),
            asset_type=data.get('asset_type', 'stock'),
            is_active=1
        )
        db.add(ticker)
        db.commit()
        return jsonify(ticker.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()


@api.route('/tickers/<ticker>', methods=['DELETE'])
def delete_ticker(ticker):
    """Delete a ticker."""
    db = SessionLocal()
    try:
        ticker_obj = db.query(TickerConfig).filter_by(ticker=ticker.upper()).first()
        if ticker_obj:
            db.delete(ticker_obj)
            db.commit()
            return jsonify({'message': 'Ticker deleted'}), 200
        return jsonify({'error': 'Ticker not found'}), 404
    finally:
        db.close()


@api.route('/articles', methods=['GET'])
def get_articles():
    """Get all articles with optional filtering."""
    ticker = request.args.get('ticker')
    limit = request.args.get('limit', 100, type=int)
    sentiment = request.args.get('sentiment')

    db = SessionLocal()
    try:
        query = db.query(NewsArticle)

        if ticker:
            query = query.filter_by(ticker=ticker.upper())

        if sentiment:
            query = query.filter_by(sentiment_label=sentiment.upper())

        articles = query.order_by(desc(NewsArticle.created_at)).limit(limit).all()
        return jsonify([article.to_dict() for article in articles])
    finally:
        db.close()


@api.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get a specific article by ID."""
    db = SessionLocal()
    try:
        article = db.query(NewsArticle).filter_by(id=article_id).first()
        if article:
            return jsonify(article.to_dict())
        return jsonify({'error': 'Article not found'}), 404
    finally:
        db.close()


@api.route('/sentiment/summary', methods=['GET'])
def sentiment_summary():
    """Get sentiment summary statistics."""
    ticker = request.args.get('ticker')
    days = request.args.get('days', 7, type=int)

    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(
            NewsArticle.sentiment_label,
            func.count(NewsArticle.id).label('count'),
            func.avg(NewsArticle.sentiment_score).label('avg_score')
        ).filter(NewsArticle.created_at >= cutoff_date)

        if ticker:
            query = query.filter_by(ticker=ticker.upper())

        results = query.group_by(NewsArticle.sentiment_label).all()

        summary = {
            'ticker': ticker.upper() if ticker else 'ALL',
            'period_days': days,
            'sentiments': [
                {
                    'label': row[0],
                    'count': row[1],
                    'avg_score': round(row[2], 4) if row[2] else 0
                }
                for row in results
            ]
        }

        return jsonify(summary)
    finally:
        db.close()


@api.route('/process', methods=['POST'])
def process_news():
    """
    Trigger news processing for specified tickers.

    Body:
        {
            "tickers": ["GME", "TSLA"] or "all",
            "max_articles": 10
        }
    """
    data = request.json
    tickers = data.get('tickers', 'all')
    max_articles = data.get('max_articles', 10)

    pipeline = NewsPipeline()

    try:
        if tickers == 'all':
            results = pipeline.process_all_active_tickers(max_articles=max_articles)
        else:
            results = {}
            for ticker in tickers:
                articles = pipeline.process_ticker(ticker, max_articles=max_articles)
                results[ticker] = articles

        # Convert to serializable format
        response = {
            ticker: [
                {
                    'title': a.get('title'),
                    'summary': a.get('summary'),
                    'sentiment_label': a.get('sentiment_label'),
                    'sentiment_score': a.get('sentiment_score'),
                    'url': a.get('url')
                }
                for a in articles
            ]
            for ticker, articles in results.items()
        }

        return jsonify({
            'status': 'success',
            'processed_tickers': list(results.keys()),
            'results': response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        pipeline.cleanup()


@api.route('/ticker/<ticker>/latest', methods=['GET'])
def get_ticker_latest(ticker):
    """Get latest articles for a specific ticker."""
    limit = request.args.get('limit', 10, type=int)

    db = SessionLocal()
    try:
        articles = db.query(NewsArticle).filter_by(
            ticker=ticker.upper()
        ).order_by(desc(NewsArticle.created_at)).limit(limit).all()

        if not articles:
            return jsonify({'message': 'No articles found', 'articles': []})

        return jsonify({
            'ticker': ticker.upper(),
            'count': len(articles),
            'articles': [article.to_dict() for article in articles]
        })
    finally:
        db.close()
