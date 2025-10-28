import React from 'react';
import { Link } from 'react-router-dom';
import './TickerCard.css';

function TickerCard({ ticker, sentimentData }) {
  const getSentimentCounts = () => {
    if (!sentimentData || !sentimentData.sentiments) {
      return { positive: 0, negative: 0, total: 0 };
    }

    const positive = sentimentData.sentiments.find(s => s.label === 'POSITIVE');
    const negative = sentimentData.sentiments.find(s => s.label === 'NEGATIVE');

    return {
      positive: positive ? positive.count : 0,
      negative: negative ? negative.count : 0,
      total: (positive?.count || 0) + (negative?.count || 0)
    };
  };

  const getSentimentPercentage = () => {
    const counts = getSentimentCounts();
    if (counts.total === 0) return 50;
    return Math.round((counts.positive / counts.total) * 100);
  };

  const counts = getSentimentCounts();
  const positivePercentage = getSentimentPercentage();

  return (
    <Link to={`/ticker/${ticker.ticker}`} className="ticker-card">
      <div className="ticker-card-header">
        <h3>{ticker.ticker}</h3>
        <span className={`asset-type ${ticker.asset_type}`}>{ticker.asset_type}</span>
      </div>

      <div className="ticker-card-body">
        <h4>{ticker.name}</h4>

        <div className="sentiment-summary">
          <div className="sentiment-bar">
            <div
              className="sentiment-bar-fill positive"
              style={{ width: `${positivePercentage}%` }}
            ></div>
          </div>

          <div className="sentiment-counts">
            <div className="sentiment-count positive">
              <span className="count">{counts.positive}</span>
              <span className="label">Positive</span>
            </div>
            <div className="sentiment-count negative">
              <span className="count">{counts.negative}</span>
              <span className="label">Negative</span>
            </div>
          </div>
        </div>

        {counts.total > 0 && (
          <div className="sentiment-percentage">
            {positivePercentage}% Positive Sentiment
          </div>
        )}

        {counts.total === 0 && (
          <div className="no-data">No recent articles</div>
        )}
      </div>
    </Link>
  );
}

export default TickerCard;
