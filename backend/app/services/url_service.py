import httpx
from typing import Dict, Any
from fastapi import HTTPException, status
from app.utils.security import validate_url_security
from app.preprocessing.metadata_processor import MetadataProcessor

class URLService:
    def __init__(self):
        self.metadata_processor = MetadataProcessor()

    async def fetch_and_extract(self, url: str) -> Dict[str, Any]:
        """Validates security boundaries and extracts article text and metadata from URL."""
        valid_url = validate_url_security(url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 MultimodalFakeNewsDetector/0.1"
        }

        try:
            async with httpx.AsyncClient(timeout=5.0, follow_redirects=True, max_redirects=3) as client:
                response = await client.get(valid_url, headers=headers)
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Target URL returned non-200 HTTP status code ({response.status_code})."
                    )

                # Check max response size (5MB max)
                content_length = response.headers.get("content-length")
                if content_length and int(content_length) > 5 * 1024 * 1024:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="URL content exceeds max allowed size of 5MB."
                    )

                html_text = response.text
                extracted = self.metadata_processor.extract_from_html(html_text, valid_url)

                if not extracted["extracted_text"] and not extracted["title"]:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Could not extract readable article text or title from the provided URL."
                    )

                return extracted

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Request to target URL timed out."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to reach target URL: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error scraping URL content: {str(e)}"
            )

url_service = URLService()
