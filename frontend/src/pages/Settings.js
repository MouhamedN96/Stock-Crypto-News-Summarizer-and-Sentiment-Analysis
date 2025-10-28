import React, { useState, useEffect } from 'react';
import { getTickers, addTicker, deleteTicker } from '../services/api';
import './Settings.css';

function Settings() {
  const [tickers, setTickers] = useState([]);
  const [newTicker, setNewTicker] = useState({
    ticker: '',
    name: '',
    asset_type: 'stock'
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    loadTickers();
  }, []);

  const loadTickers = async () => {
    try {
      const res = await getTickers();
      setTickers(res.data);
    } catch (err) {
      setError('Failed to load tickers: ' + err.message);
    }
  };

  const handleAddTicker = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      setSuccess(null);
      await addTicker(newTicker);
      setSuccess('Ticker added successfully!');
      setNewTicker({ ticker: '', name: '', asset_type: 'stock' });
      loadTickers();
    } catch (err) {
      setError('Failed to add ticker: ' + err.message);
    }
  };

  const handleDeleteTicker = async (ticker) => {
    if (window.confirm(`Are you sure you want to delete ${ticker}?`)) {
      try {
        setError(null);
        await deleteTicker(ticker);
        setSuccess('Ticker deleted successfully!');
        loadTickers();
      } catch (err) {
        setError('Failed to delete ticker: ' + err.message);
      }
    }
  };

  return (
    <div className="settings">
      <h1>Settings</h1>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="card">
        <h2>Add New Ticker</h2>
        <form onSubmit={handleAddTicker} className="ticker-form">
          <div className="form-group">
            <label>Ticker Symbol</label>
            <input
              type="text"
              value={newTicker.ticker}
              onChange={(e) => setNewTicker({ ...newTicker, ticker: e.target.value.toUpperCase() })}
              placeholder="e.g., AAPL"
              required
            />
          </div>

          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={newTicker.name}
              onChange={(e) => setNewTicker({ ...newTicker, name: e.target.value })}
              placeholder="e.g., Apple Inc."
              required
            />
          </div>

          <div className="form-group">
            <label>Asset Type</label>
            <select
              value={newTicker.asset_type}
              onChange={(e) => setNewTicker({ ...newTicker, asset_type: e.target.value })}
            >
              <option value="stock">Stock</option>
              <option value="crypto">Crypto</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary">Add Ticker</button>
        </form>
      </div>

      <div className="card">
        <h2>Monitored Tickers</h2>
        <div className="ticker-list">
          {tickers.map(ticker => (
            <div key={ticker.id} className="ticker-item">
              <div className="ticker-info">
                <strong>{ticker.ticker}</strong>
                <span>{ticker.name}</span>
                <span className="ticker-type">{ticker.asset_type}</span>
              </div>
              <button
                className="btn btn-danger btn-sm"
                onClick={() => handleDeleteTicker(ticker.ticker)}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Settings;
