import React from 'react';
import './ArticleList.css';

function ArticleList({ articles }) {
  const getSentimentClass = (label) => {
    if (!label) return 'sentiment-neutral';
    const lower = label.toLowerCase();
    if (lower === 'positive') return 'sentiment-positive';
    if (lower === 'negative') return 'sentiment-negative';
    return 'sentiment-neutral';
  };

  if (!articles || articles.length === 0) {
    return <div className="no-articles">No articles found</div>;
  }

  return (
    <div className="article-list">
      {articles.map((article, index) => (
        <div key={article.id || index} className="article-item">
          <div className="article-header">
            <h3>{article.title || 'Untitled'}</h3>
            <span className={`sentiment-badge ${getSentimentClass(article.sentiment_label)}`}>
              {article.sentiment_label || 'N/A'}
              {article.sentiment_score && ` (${(article.sentiment_score * 100).toFixed(1)}%)`}
            </span>
          </div>

          <div className="article-summary">
            {article.summary || article.content?.substring(0, 200) + '...'}
          </div>

          <div className="article-footer">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="article-link"
            >
              Read Full Article →
            </a>
            {article.created_at && (
              <span className="article-date">
                {new Date(article.created_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ArticleList;
