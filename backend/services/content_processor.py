import tiktoken
import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self):
        # Initialize tokenizer for GPT-4
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 300  # Smaller chunks to get more results
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def split_text_into_chunks(self, text: str, max_tokens: int = 300) -> List[str]:
        """Split text into chunks with maximum token limit"""
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if adding this sentence would exceed the limit
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            if self.count_tokens(test_chunk) <= max_tokens:
                current_chunk = test_chunk
            else:
                # If current chunk has content, save it
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # If single sentence is too long, split it by words
                    words = sentence.split()
                    temp_chunk = ""
                    for word in words:
                        test_word_chunk = temp_chunk + " " + word if temp_chunk else word
                        if self.count_tokens(test_word_chunk) <= max_tokens:
                            temp_chunk = test_word_chunk
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                                temp_chunk = word
                            else:
                                # Single word is too long, truncate it
                                chunks.append(word[:100] + "...")
                    current_chunk = temp_chunk
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_content(self, html_content: str, url: str) -> List[Dict]:
        """
        Process HTML content into searchable chunks
        """
        try:
            logger.info(f"Processing content from {url}")
            
            # Split content into chunks
            text_chunks = self.split_text_into_chunks(html_content, self.max_tokens)
            
            # Create chunk objects with metadata
            chunks = []
            for i, chunk_text in enumerate(text_chunks):
                if not chunk_text.strip():
                    continue
                    
                chunk = {
                    "id": f"{url}_{i}",
                    "content": chunk_text,
                    "url": url,
                    "chunk_index": i,
                    "token_count": self.count_tokens(chunk_text),
                    "title": self.extract_title(chunk_text),
                    "metadata": {
                        "source_url": url,
                        "chunk_id": i,
                        "token_count": self.count_tokens(chunk_text)
                    }
                }
                chunks.append(chunk)
            
            logger.info(f"Created {len(chunks)} chunks from {url}")
            
            # Log chunk details for debugging
            if chunks:
                avg_tokens = sum(chunk['token_count'] for chunk in chunks) / len(chunks)
                logger.info(f"Average tokens per chunk: {avg_tokens:.1f}")
                logger.info(f"First chunk preview: {chunks[0]['content'][:100]}...")
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
            raise Exception(f"Failed to process content: {str(e)}")
    
    def extract_title(self, text: str) -> str:
        """Extract a title from chunk text"""
        # Take first sentence or first 100 characters
        sentences = re.split(r'[.!?]+', text)
        first_sentence = sentences[0].strip() if sentences else ""
        
        if len(first_sentence) > 100:
            return first_sentence[:100] + "..."
        elif first_sentence:
            return first_sentence
        else:
            return "Content Chunk"
