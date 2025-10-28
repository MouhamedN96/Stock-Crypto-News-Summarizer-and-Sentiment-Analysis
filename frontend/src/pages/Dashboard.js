import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getTickers, getSentimentSummary, processNews } from '../services/api';
import SentimentChart from '../components/SentimentChart';
import TickerCard from '../components/TickerCard';
import './Dashboard.css';

function Dashboard() {
  const [tickers, setTickers] = useState([]);
  const [sentimentData, setSentimentData] = useState({});
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load tickers
      const tickersRes = await getTickers();
      setTickers(tickersRes.data);

      // Load sentiment data for each ticker
      const sentimentPromises = tickersRes.data.map(ticker =>
        getSentimentSummary(ticker.ticker, 7)
      );
      const sentimentResults = await Promise.all(sentimentPromises);

      const sentimentMap = {};
      sentimentResults.forEach(res => {
        sentimentMap[res.data.ticker] = res.data;
      });
      setSentimentData(sentimentMap);

      setLoading(false);
    } catch (err) {
      setError('Failed to load data: ' + err.message);
      setLoading(false);
    }
  };

  const handleProcessNews = async () => {
    try {
      setProcessing(true);
      setError(null);
      setSuccessMessage(null);

      await processNews('all', 10);

      setSuccessMessage('Successfully processed news for all tickers!');

      // Reload data after processing
      setTimeout(() => {
        loadData();
        setSuccessMessage(null);
      }, 2000);

    } catch (err) {
      setError('Failed to process news: ' + err.message);
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
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Market Sentiment Dashboard</h1>
        <button
          className="btn btn-primary"
          onClick={handleProcessNews}
          disabled={processing}
        >
          {processing ? 'Processing...' : 'Update All News'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <div className="ticker-grid">
        {tickers.map(ticker => (
          <TickerCard
            key={ticker.id}
            ticker={ticker}
            sentimentData={sentimentData[ticker.ticker]}
          />
        ))}
      </div>

      {tickers.length > 0 && (
        <div className="card">
          <h2>Overall Sentiment Trends</h2>
          <SentimentChart data={sentimentData} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
