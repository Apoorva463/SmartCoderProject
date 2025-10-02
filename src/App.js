import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (url, query) => {
    console.log('🔍 Starting search with:', { url, query });
    setLoading(true);
    setError(null);
    setResults([]);

    try {
      console.log('📡 Making API request to /api/search');
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, query }),
      });

      console.log('📨 Response status:', response.status);
      console.log('📨 Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('📦 Full API Response:', JSON.stringify(data, null, 2));
      console.log('📊 Number of results received:', data.results ? data.results.length : 0);
      console.log('📋 Results array:', data.results);
      
      setResults(data.results || []);
      console.log('✅ Results set in state');
    } catch (err) {
      console.error('❌ Search error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
      console.log('🏁 Search completed');
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
