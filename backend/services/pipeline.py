"""Main pipeline orchestrating news scraping, summarization, and sentiment analysis."""

from typing import List, Dict
from backend.services.news_scraper import NewsScraper
from backend.services.summarizer import NewsSummarizer
from backend.services.sentiment_analyzer import SentimentAnalyzer
from backend.models.news_article import NewsArticle, TickerConfig
from backend.config.database import SessionLocal


class NewsPipeline:
    """Complete pipeline for processing news articles."""

    def __init__(self):
        self.scraper = NewsScraper()
        self.summarizer = NewsSummarizer()
        self.sentiment_analyzer = SentimentAnalyzer()

    def process_ticker(self, ticker: str, max_articles: int = 10, save_to_db: bool = True) -> List[Dict]:
        """
        Process news articles for a ticker.

        Args:
            ticker: Stock/crypto ticker symbol
            max_articles: Maximum number of articles to process
            save_to_db: Whether to save results to database

        Returns:
            List of processed article dictionaries
        """
        print(f"\n{'='*60}")
        print(f"Processing ticker: {ticker}")
        print(f"{'='*60}")

        # Step 1: Scrape news articles
        print(f"[1/3] Scraping news articles...")
        articles = self.scraper.scrape_ticker_news(ticker, max_articles=max_articles)
        print(f"Found {len(articles)} articles")

        if not articles:
            print(f"No articles found for {ticker}")
            return []

        # Step 2: Summarize articles
        print(f"[2/3] Summarizing articles...")
        self.summarizer.load_model()
        for i, article in enumerate(articles):
            summary = self.summarizer.summarize(article['content'])
            article['summary'] = summary
            print(f"Summarized article {i+1}/{len(articles)}")

        # Step 3: Analyze sentiment
        print(f"[3/3] Analyzing sentiment...")
        self.sentiment_analyzer.load_model()
        for i, article in enumerate(articles):
            sentiment = self.sentiment_analyzer.analyze(article['summary'])
            article['sentiment_label'] = sentiment['label']
            article['sentiment_score'] = sentiment['score']
            print(f"Analyzed sentiment {i+1}/{len(articles)}: {sentiment['label']} ({sentiment['score']:.2f})")

        # Step 4: Save to database
        if save_to_db:
            print(f"[4/4] Saving to database...")
            self._save_to_database(ticker, articles)
            print(f"Saved {len(articles)} articles to database")

        print(f"\nCompleted processing {ticker}")
        return articles

    def _save_to_database(self, ticker: str, articles: List[Dict]):
        """Save processed articles to database."""
        db = SessionLocal()
        try:
            for article in articles:
                # Check if article already exists
                existing = db.query(NewsArticle).filter_by(url=article['url']).first()

                if existing:
                    # Update existing article
                    existing.summary = article.get('summary')
                    existing.sentiment_label = article.get('sentiment_label')
                    existing.sentiment_score = article.get('sentiment_score')
                else:
                    # Create new article
                    news_article = NewsArticle(
                        ticker=ticker,
                        url=article['url'],
                        title=article.get('title'),
                        content=article.get('content'),
                        summary=article.get('summary'),
                        sentiment_label=article.get('sentiment_label'),
                        sentiment_score=article.get('sentiment_score')
                    )
                    db.add(news_article)

            db.commit()

        except Exception as e:
            print(f"Error saving to database: {e}")
            db.rollback()
        finally:
            db.close()

    def process_all_active_tickers(self, max_articles: int = 10) -> Dict[str, List[Dict]]:
        """
        Process all active tickers from database.

        Args:
            max_articles: Maximum number of articles per ticker

        Returns:
            Dictionary mapping ticker to list of processed articles
        """
        db = SessionLocal()
        results = {}

        try:
            # Get all active tickers
            tickers = db.query(TickerConfig).filter_by(is_active=1).all()

            for ticker_config in tickers:
                ticker = ticker_config.ticker
                articles = self.process_ticker(ticker, max_articles=max_articles)
                results[ticker] = articles

        except Exception as e:
            print(f"Error processing tickers: {e}")
        finally:
            db.close()

        return results

    def cleanup(self):
        """Cleanup models from memory."""
        self.summarizer.unload_model()
        self.sentiment_analyzer.unload_model()
