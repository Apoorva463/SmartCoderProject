from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from services.content_fetcher import ContentFetcher
from services.content_processor import ContentProcessor
from services.vector_search import VectorSearch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Website Content Search API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
content_fetcher = ContentFetcher()
content_processor = ContentProcessor()
vector_search = VectorSearch()

class SearchRequest(BaseModel):
    url: str
    query: str

class SearchResponse(BaseModel):
    results: list
    total_chunks: int
    query: str
    url: str

@app.get("/")
async def root():
    return {"message": "Website Content Search API"}

@app.post("/api/search", response_model=SearchResponse)
async def search_content(request: SearchRequest):
    try:
        logger.info(f"Processing search request for URL: {request.url}")
        
        # Fetch HTML content
        html_content = await content_fetcher.fetch_content(request.url)
        if not html_content:
            raise HTTPException(status_code=400, detail="Failed to fetch content from URL")
        
        # Process content into chunks
        chunks = content_processor.process_content(html_content, request.url)
        logger.info(f"Created {len(chunks)} content chunks")
        
        # Perform vector search
        results = await vector_search.search_similar_chunks(request.query, chunks)
        logger.info(f"Found {len(results)} relevant results")
        
        return SearchResponse(
            results=results,
            total_chunks=len(chunks),
            query=request.query,
            url=request.url
        )
        
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
