import numpy as np
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import logging
from typing import List, Dict
import hashlib

logger = logging.getLogger(__name__)

class VectorSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        self.collection_name = "website_content"
        self.connect_to_milvus()
        self.setup_collection()
    
    def connect_to_milvus(self):
        """Connect to Milvus vector database"""
        try:
            # Connect to Milvus (assuming it's running locally)
            connections.connect("default", host="localhost", port="19530")
            logger.info("Connected to Milvus")
        except Exception as e:
            logger.warning(f"Could not connect to Milvus: {e}")
            logger.info("Running in fallback mode without vector database")
            self.milvus_available = False
            return
        
        self.milvus_available = True
    
    def setup_collection(self):
        """Setup Milvus collection for storing embeddings"""
        if not self.milvus_available:
            return
            
        try:
            # Check if collection exists
            if utility.has_collection(self.collection_name):
                self.collection = Collection(self.collection_name)
                logger.info(f"Using existing collection: {self.collection_name}")
            else:
                # Create collection schema
                fields = [
                    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=10000),
                    FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500),
                    FieldSchema(name="chunk_index", dtype=DataType.INT64),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
                ]
                
                schema = CollectionSchema(fields, "Website content chunks with embeddings")
                self.collection = Collection(self.collection_name, schema)
                
                # Create index
                index_params = {
                    "metric_type": "L2",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 128}
                }
                self.collection.create_index("embedding", index_params)
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error setting up collection: {e}")
            self.milvus_available = False
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence transformer"""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return [0.0] * self.embedding_dim
    
    def index_chunks(self, chunks: List[Dict]):
        """Index chunks in vector database"""
        if not self.milvus_available:
            logger.info("Milvus not available, skipping indexing")
            return
        
        try:
            # Prepare data for insertion
            ids = []
            contents = []
            urls = []
            chunk_indices = []
            embeddings = []
            
            for chunk in chunks:
                ids.append(chunk["id"])
                contents.append(chunk["content"])
                urls.append(chunk["url"])
                chunk_indices.append(chunk["chunk_index"])
                embeddings.append(self.generate_embedding(chunk["content"]))
            
            # Insert data
            data = [ids, contents, urls, chunk_indices, embeddings]
            self.collection.insert(data)
            self.collection.flush()
            logger.info(f"Indexed {len(chunks)} chunks in vector database")
            
        except Exception as e:
            logger.error(f"Error indexing chunks: {e}")
    
    async def search_similar_chunks(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """Search for similar chunks using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            if self.milvus_available:
                return await self._vector_search(query, query_embedding, chunks)
            else:
                return await self._fallback_search(query, chunks)
                
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return await self._fallback_search(query, chunks)
    
    async def _vector_search(self, query: str, query_embedding: List[float], chunks: List[Dict]) -> List[Dict]:
        """Perform vector search using Milvus"""
        try:
            # Index chunks first
            self.index_chunks(chunks)
            
            # Load collection
            self.collection.load()
            
            # Search parameters
            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
            
            # Perform search
            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=10,
                output_fields=["content", "url", "chunk_index"]
            )
            
            # Format results
            formatted_results = []
            for hit in results[0]:
                result = {
                    "content": hit.entity.get("content"),
                    "url": hit.entity.get("url"),
                    "chunk_index": hit.entity.get("chunk_index"),
                    "score": 1.0 / (1.0 + hit.distance),  # Convert distance to similarity score
                    "title": self._extract_title(hit.entity.get("content"))
                }
                formatted_results.append(result)
            
            return formatted_results[:10]
            
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return await self._fallback_search(query, chunks)
    
    async def _fallback_search(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """Fallback search using text similarity when vector DB is not available"""
        try:
            query_lower = query.lower()
            query_words = set(query_lower.split())
            
            scored_chunks = []
            
            for chunk in chunks:
                content_lower = chunk["content"].lower()
                content_words = set(content_lower.split())
                
                # Calculate similarity score
                word_overlap = len(query_words.intersection(content_words))
                total_words = len(query_words.union(content_words))
                
                # Jaccard similarity
                jaccard_score = word_overlap / total_words if total_words > 0 else 0
                
                # Keyword frequency score
                keyword_count = sum(1 for word in query_words if word in content_lower)
                frequency_score = keyword_count / len(query_words) if query_words else 0
                
                # Combined score
                combined_score = (jaccard_score * 0.6) + (frequency_score * 0.4)
                
                scored_chunks.append({
                    "content": chunk["content"],
                    "url": chunk["url"],
                    "chunk_index": chunk["chunk_index"],
                    "score": combined_score,
                    "title": chunk.get("title", self._extract_title(chunk["content"]))
                })
            
            # Sort by score and return top 10
            scored_chunks.sort(key=lambda x: x["score"], reverse=True)
            return scored_chunks[:10]
            
        except Exception as e:
            logger.error(f"Error in fallback search: {e}")
            return []
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content"""
        if not content:
            return "Content Chunk"
        
        # Take first sentence or first 100 characters
        sentences = content.split('.')
        first_sentence = sentences[0].strip() if sentences else ""
        
        if len(first_sentence) > 100:
            return first_sentence[:100] + "..."
        elif first_sentence:
            return first_sentence
        else:
            return content[:100] + "..." if len(content) > 100 else content
