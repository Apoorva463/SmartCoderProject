import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

class ContentFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def fetch_content(self, url: str) -> str:
        """
        Fetch HTML content from the given URL
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # Add https if no scheme provided
            if not parsed_url.scheme:
                url = f"https://{url}"
            
            logger.info(f"Fetching content from: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text content
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            logger.info(f"Successfully fetched {len(text)} characters of content")
            return text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching {url}: {str(e)}")
            raise Exception(f"Failed to fetch content: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            raise Exception(f"Error processing content: {str(e)}")
