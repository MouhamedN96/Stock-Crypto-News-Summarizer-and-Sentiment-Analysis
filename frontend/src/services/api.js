import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Tickers
export const getTickers = () => api.get('/tickers');
export const addTicker = (ticker) => api.post('/tickers', ticker);
export const deleteTicker = (ticker) => api.delete(`/tickers/${ticker}`);

// Articles
export const getArticles = (params = {}) => api.get('/articles', { params });
export const getArticle = (id) => api.get(`/articles/${id}`);
export const getTickerLatest = (ticker, limit = 10) =>
  api.get(`/ticker/${ticker}/latest`, { params: { limit } });

// Sentiment
export const getSentimentSummary = (ticker = null, days = 7) =>
  api.get('/sentiment/summary', { params: { ticker, days } });

// Processing
export const processNews = (tickers = 'all', maxArticles = 10) =>
  api.post('/process', { tickers, max_articles: maxArticles });

// Health
export const healthCheck = () => api.get('/health');

export default api;
