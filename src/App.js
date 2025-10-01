import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (url, query) => {
    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Website Content Search</h1>
        <p>Enter a website URL and search query to find relevant content chunks</p>
      </header>
      
      <main className="App-main">
        <SearchForm onSearch={handleSearch} loading={loading} />
        
        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}
        
        <SearchResults results={results} loading={loading} />
      </main>
    </div>
  );
}

export default App;
