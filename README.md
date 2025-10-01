# Website Content Search Application

A single-page application that allows users to input a website URL and search query to find the top 10 most relevant content chunks from the website.

## Features

- **Frontend**: React-based SPA with modern UI
- **Backend**: Python FastAPI with semantic search capabilities
- **Vector Database**: Milvus integration for semantic search
- **Content Processing**: Automatic HTML parsing and chunking (500 tokens max per chunk)
- **Search**: Semantic search with fallback to text-based similarity

## Architecture

```
Frontend (React) → Backend (FastAPI) → Vector DB (Milvus) → Content Processing
```

## Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Milvus vector database (optional, fallback available)

## Installation

### 1. Install Dependencies

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
# The setup script will create a virtual environment automatically
./setup.sh
```

### 2. Setup Milvus (Optional)

For full semantic search capabilities, install and run Milvus:

```bash
# Using Docker
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  -v $(pwd)/volumes/milvus:/var/lib/milvus \
  milvusdb/milvus:latest
```

If Milvus is not available, the application will automatically fall back to text-based similarity search.

## Running the Application

### 1. Start the Backend

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Start the Frontend

```bash
npm start
```

The React app will be available at `http://localhost:3000`

## API Endpoints

- `GET /` - API health check
- `POST /api/search` - Search for content chunks
- `GET /health` - Health check endpoint

### Search Request Format

```json
{
  "url": "https://example.com",
  "query": "your search query"
}
```

### Search Response Format

```json
{
  "results": [
    {
      "content": "chunk content...",
      "url": "https://example.com",
      "chunk_index": 0,
      "score": 0.85,
      "title": "Content Title"
    }
  ],
  "total_chunks": 25,
  "query": "your search query",
  "url": "https://example.com"
}
```

## How It Works

1. **Content Fetching**: The backend fetches HTML content from the provided URL
2. **Content Processing**: HTML is parsed and split into chunks of maximum 500 tokens
3. **Vector Indexing**: Chunks are embedded using sentence transformers and indexed in Milvus
4. **Semantic Search**: Query is embedded and matched against chunk embeddings
5. **Ranking**: Results are ranked by similarity score and top 10 are returned

## Fallback Mode

If Milvus is not available, the application automatically falls back to:
- Text-based similarity using Jaccard similarity
- Keyword frequency matching
- Combined scoring algorithm

## Development

### Project Structure

```
├── src/                    # React frontend
│   ├── components/        # React components
│   ├── App.js            # Main app component
│   └── index.js          # Entry point
├── backend/              # Python backend
│   ├── services/         # Business logic services
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
└── package.json        # Node.js dependencies
```

### Adding New Features

1. **Frontend**: Add new components in `src/components/`
2. **Backend**: Add new services in `backend/services/`
3. **API**: Add new endpoints in `backend/main.py`

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend is running on port 8000
2. **Milvus Connection**: Check if Milvus is running on localhost:19530
3. **Content Fetching**: Some websites may block automated requests

### Logs

Check the console output for detailed error messages and processing logs.

## License

MIT License
