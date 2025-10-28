# Stock & Crypto News Sentiment Analysis Platform

A full-stack application that scrapes, summarizes, and analyzes sentiment of news articles for stocks and cryptocurrencies using state-of-the-art NLP models.

## Features

- **Automated News Scraping**: Searches and scrapes financial news from Yahoo Finance and other sources
- **AI-Powered Summarization**: Uses Pegasus transformer model fine-tuned for financial text
- **Sentiment Analysis**: Classifies articles as POSITIVE/NEGATIVE with confidence scores
- **Interactive Dashboard**: Real-time visualization of sentiment trends
- **RESTful API**: Easy integration with other tools and services
- **Database Storage**: SQLite or PostgreSQL for persistent data
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Tech Stack

### Backend
- **Python 3.10+**
- **Flask**: REST API framework
- **SQLAlchemy**: ORM for database management
- **Transformers (HuggingFace)**: Pre-trained NLP models
- **BeautifulSoup**: Web scraping
- **PyTorch**: Deep learning framework

### Frontend
- **React 18**: Modern UI framework
- **React Router**: Client-side routing
- **Chart.js**: Data visualization
- **Axios**: HTTP client

### Database
- **SQLite**: Default (development)
- **PostgreSQL**: Production-ready option

## Project Structure

```
Stock-Crypto-News-Summarizer-and-Sentiment-Analysis/
├── backend/
│   ├── models/           # Database models
│   │   └── news_article.py
│   ├── services/         # Business logic
│   │   ├── news_scraper.py
│   │   ├── summarizer.py
│   │   ├── sentiment_analyzer.py
│   │   └── pipeline.py
│   ├── routes/           # API routes
│   │   └── api.py
│   ├── config/           # Configuration
│   │   └── database.py
│   └── app.py            # Flask app entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── App.js
│   ├── public/
│   └── package.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Stock-Crypto-News-Summarizer-and-Sentiment-Analysis
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000 (if running dev profile)
   - Backend API: http://localhost:5000

### Option 2: Manual Setup

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the backend**
   ```bash
   python -m backend.app
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Usage

### Web Interface

1. **Dashboard**: View sentiment overview for all monitored tickers
2. **Ticker Details**: Click on any ticker to see detailed articles
3. **Settings**: Add or remove tickers to monitor
4. **Update News**: Click "Update All News" to fetch latest articles

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Get All Tickers
```bash
GET /api/tickers
```

#### Add New Ticker
```bash
POST /api/tickers
Content-Type: application/json

{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "asset_type": "stock"
}
```

#### Get Articles
```bash
GET /api/articles?ticker=GME&limit=10
```

#### Get Sentiment Summary
```bash
GET /api/sentiment/summary?ticker=BTC&days=7
```

#### Process News
```bash
POST /api/process
Content-Type: application/json

{
  "tickers": ["GME", "TSLA"],  // or "all"
  "max_articles": 10
}
```

#### Get Latest Articles for Ticker
```bash
GET /api/ticker/GME/latest?limit=10
```

## Models

### Summarization Model
- **Model**: `human-centered-summarization/financial-summarization-pegasus`
- **Purpose**: Generates concise summaries of financial news articles
- **Max Output**: 55 tokens (configurable)

### Sentiment Model
- **Model**: Default HuggingFace sentiment-analysis pipeline
- **Purpose**: Classifies text as POSITIVE or NEGATIVE
- **Output**: Label + confidence score (0-1)

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=sqlite:///./news_sentiment.db

# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5000

# Models
SUMMARIZATION_MODEL=human-centered-summarization/financial-summarization-pegasus
SENTIMENT_MODEL=default

# Processing
MAX_ARTICLES_PER_TICKER=10
DEFAULT_SUMMARY_LENGTH=55
```

## Development

### Running Tests
```bash
# Backend tests (when implemented)
pytest backend/tests/

# Frontend tests
cd frontend
npm test
```

### Code Structure

#### Backend Services

1. **NewsScraper** (`news_scraper.py`)
   - Searches Google for news URLs
   - Scrapes article content
   - Filters and cleans data

2. **NewsSummarizer** (`summarizer.py`)
   - Loads Pegasus model
   - Generates article summaries
   - Manages model lifecycle

3. **SentimentAnalyzer** (`sentiment_analyzer.py`)
   - Performs sentiment classification
   - Returns labels and confidence scores

4. **NewsPipeline** (`pipeline.py`)
   - Orchestrates the complete workflow
   - Manages database interactions
   - Coordinates all services

## Database Schema

### NewsArticle
- `id`: Primary key
- `ticker`: Stock/crypto symbol
- `url`: Article URL (unique)
- `title`: Article title
- `content`: Full article text
- `summary`: Generated summary
- `sentiment_label`: POSITIVE/NEGATIVE
- `sentiment_score`: Confidence (0-1)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### TickerConfig
- `id`: Primary key
- `ticker`: Symbol (unique)
- `name`: Full name
- `asset_type`: 'stock' or 'crypto'
- `is_active`: Boolean
- `created_at`: Timestamp

## Deployment

### Production Deployment (Docker)

1. **Update docker-compose.yml for production**
   ```yaml
   # Use PostgreSQL
   DATABASE_URL: postgresql://user:pass@db:5432/news_sentiment
   FLASK_ENV: production
   ```

2. **Build and deploy**
   ```bash
   docker-compose up -d --build
   ```

3. **Use a reverse proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Using Gunicorn (Production WSGI Server)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## Performance Considerations

- **Model Loading**: Models are loaded on-demand and cached
- **Batch Processing**: Articles are processed sequentially to manage memory
- **Database**: Use PostgreSQL for production environments
- **Caching**: Consider adding Redis for API response caching

## Troubleshooting

### Model Download Issues
If models fail to download, manually download them:
```python
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
model = PegasusForConditionalGeneration.from_pretrained("human-centered-summarization/financial-summarization-pegasus")
```

### CORS Issues
Ensure Flask-CORS is properly configured in `backend/app.py`

### Database Migration
To reset the database:
```bash
rm news_sentiment.db
python -m backend.app  # Will recreate tables
```

## Future Enhancements

- [ ] Real-time news updates with WebSockets
- [ ] Historical sentiment tracking and trends
- [ ] Multi-language support
- [ ] Advanced filtering and search
- [ ] Email/SMS alerts for sentiment changes
- [ ] Integration with trading APIs
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- HuggingFace Transformers for pre-trained models
- Yahoo Finance for news content
- Open-source community for amazing tools

## Contact

For questions or support, please open an issue on GitHub.

---

**Status**: Production-ready with full-stack implementation, database integration, and Docker support.
