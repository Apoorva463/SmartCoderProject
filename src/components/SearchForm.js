import React, { useState } from 'react';
import './SearchForm.css';

const SearchForm = ({ onSearch, loading }) => {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim() && query.trim()) {
      onSearch(url.trim(), query.trim());
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="url">Website URL</label>
        <input
          type="url"
          id="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          required
          disabled={loading}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="query">Search Query</label>
        <input
          type="text"
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your search query..."
          required
          disabled={loading}
        />
      </div>
      
      <button 
        type="submit" 
        className="search-button"
        disabled={loading || !url.trim() || !query.trim()}
      >
        {loading ? 'Searching...' : 'Search Content'}
      </button>
    </form>
  );
};

export default SearchForm;
