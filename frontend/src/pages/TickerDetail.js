import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTickerLatest, processNews } from '../services/api';
import ArticleList from '../components/ArticleList';
import './TickerDetail.css';

function TickerDetail() {
  const { ticker } = useParams();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadArticles();
  }, [ticker]);

  const loadArticles = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getTickerLatest(ticker.toUpperCase(), 20);
      setArticles(res.data.articles || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load articles: ' + err.message);
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setProcessing(true);
      setError(null);
      await processNews([ticker.toUpperCase()], 10);
      setTimeout(loadArticles, 2000);
    } catch (err) {
      setError('Failed to refresh news: ' + err.message);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="ticker-detail">
      <div className="ticker-header">
        <h1>{ticker.toUpperCase()} News & Sentiment</h1>
        <button
          className="btn btn-primary"
          onClick={handleRefresh}
          disabled={processing}
        >
          {processing ? 'Updating...' : 'Refresh News'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="card">
        <h2>Latest Articles ({articles.length})</h2>
        <ArticleList articles={articles} />
      </div>
    </div>
  );
}

export default TickerDetail;
