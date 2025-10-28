"""Database configuration and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.models.news_article import Base

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./news_sentiment.db')

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)


def init_db():
    """Initialize database and create all tables."""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DATABASE_URL}")


def get_db():
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_default_tickers():
    """Initialize default tickers if database is empty."""
    from backend.models.news_article import TickerConfig

    db = SessionLocal()
    try:
        # Check if tickers already exist
        count = db.query(TickerConfig).count()
        if count == 0:
            default_tickers = [
                TickerConfig(ticker='GME', name='GameStop', asset_type='stock', is_active=1),
                TickerConfig(ticker='TSLA', name='Tesla', asset_type='stock', is_active=1),
                TickerConfig(ticker='BTC', name='Bitcoin', asset_type='crypto', is_active=1),
                TickerConfig(ticker='ETH', name='Ethereum', asset_type='crypto', is_active=1),
            ]
            db.add_all(default_tickers)
            db.commit()
            print("Default tickers initialized")
    except Exception as e:
        print(f"Error initializing default tickers: {e}")
        db.rollback()
    finally:
        db.close()
