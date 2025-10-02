import React from 'react';
import './SearchResults.css';

const SearchResults = ({ results, loading }) => {
  console.log('🎨 SearchResults component rendered');
  console.log('🎨 Loading state:', loading);
  console.log('🎨 Results received:', results ? results.length : 0, 'results');
  console.log('🎨 Results data:', results);
  
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Searching for relevant content...</p>
      </div>
    );
  }

  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="search-results">
      <h2>Top {results.length} Result{results.length !== 1 ? 's' : ''} (showing up to 10)</h2>
      <div className="results-grid">
        {results.map((result, index) => (
          <div key={index} className="result-card">
            <div className="result-header">
              <span className="result-rank">#{index + 1}</span>
              <span className="result-score">Score: {result.score?.toFixed(3) || 'N/A'}</span>
            </div>
            <div className="result-content">
              <h3 className="result-title">
                {result.title || `Content Chunk ${index + 1}`}
              </h3>
              <div className="result-text">
                {result.content}
              </div>
              {result.url && (
                <div className="result-meta">
                  <span className="result-url">Source: {result.url}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
