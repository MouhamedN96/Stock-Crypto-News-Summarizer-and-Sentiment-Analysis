# Setup Guide

## Quick Start

### Using Docker (Easiest)

```bash
# 1. Clone repository
git clone <repo-url>
cd Stock-Crypto-News-Summarizer-and-Sentiment-Analysis

# 2. Create environment file
cp .env.example .env

# 3. Start with Docker Compose
docker-compose up -d

# 4. Access the application
# Backend: http://localhost:5000
# Frontend: http://localhost:3000 (if dev profile)
```

### Manual Setup

#### Prerequisites
- Python 3.10+
- Node.js 18+
- pip and npm

#### Backend

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Run backend
python -m backend.app
```

Backend will be available at http://localhost:5000

#### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm start
```

Frontend will be available at http://localhost:3000

## First-Time Usage

1. **Access the dashboard**: Open http://localhost:3000

2. **Default tickers**: The app comes with GME, TSLA, BTC, ETH pre-configured

3. **Update news**: Click "Update All News" to fetch and analyze articles

4. **Add tickers**: Go to Settings to add more stocks or cryptocurrencies

5. **View details**: Click on any ticker card to see detailed articles

## Configuration

### Database Options

#### SQLite (Default - Development)
```env
DATABASE_URL=sqlite:///./news_sentiment.db
```

#### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/news_sentiment
```

### Model Configuration

```env
SUMMARIZATION_MODEL=human-centered-summarization/financial-summarization-pegasus
SENTIMENT_MODEL=default
```

### Processing Settings

```env
MAX_ARTICLES_PER_TICKER=10
DEFAULT_SUMMARY_LENGTH=55
```

## Troubleshooting

### Models not downloading
- Ensure you have internet connection
- Check if you have enough disk space (models are ~1-2GB)
- Try manually downloading models:
  ```python
  from transformers import pipeline
  pipeline('sentiment-analysis')
  ```

### Port already in use
- Change ports in `.env`:
  ```env
  PORT=5001  # Backend
  ```
- For frontend, change in `package.json`:
  ```json
  "start": "PORT=3001 react-scripts start"
  ```

### Database errors
- Delete existing database:
  ```bash
  rm news_sentiment.db
  ```
- Restart the application to recreate tables

### CORS errors
- Ensure backend is running
- Check proxy setting in `frontend/package.json`
- Verify Flask-CORS is installed

## Performance Tips

### For faster processing:
1. **Use GPU**: Install `torch` with CUDA support
2. **Reduce articles**: Lower `MAX_ARTICLES_PER_TICKER`
3. **Cache models**: Models are cached after first load
4. **Use PostgreSQL**: Better performance for large datasets

### For production:
1. **Use Gunicorn**: Replace `python -m backend.app` with:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

2. **Build frontend**: Create production build:
   ```bash
   cd frontend
   npm run build
   ```

3. **Use Docker**: Production-ready deployment:
   ```bash
   docker-compose up -d --build
   ```

## API Testing

Use curl or Postman to test the API:

```bash
# Health check
curl http://localhost:5000/api/health

# Get tickers
curl http://localhost:5000/api/tickers

# Get articles
curl http://localhost:5000/api/articles?ticker=GME

# Process news
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"tickers": "all", "max_articles": 5}'
```

## Next Steps

1. **Customize tickers**: Add your favorite stocks/crypto in Settings
2. **Schedule updates**: Set up cron job to run processing regularly
3. **Explore API**: Build integrations with the REST API
4. **Deploy**: Use Docker for production deployment

## Getting Help

- Check logs in console/terminal
- Review API responses for error details
- Open an issue on GitHub
- Check the main README.md for more information
