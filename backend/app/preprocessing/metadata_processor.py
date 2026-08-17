from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, Any

class MetadataProcessor:
    def extract_from_html(self, html_content: str, source_url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract title
        title_tag = soup.find("title")
        title = title_tag.get_text().strip() if title_tag else ""
        
        # OG Title
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()
            
        # Canonical URL
        canonical = soup.find("link", rel="canonical")
        canonical_url = canonical["href"] if canonical and canonical.get("href") else source_url
        
        # Domain name
        domain = urlparse(source_url).netloc
        
        # Extract main text paragraphs
        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 30]
        full_text = " ".join(paragraphs)
        
        # Extract main og:image if available
        og_image = soup.find("meta", property="og:image")
        image_url = og_image["content"] if og_image and og_image.get("content") else None

        return {
            "title": title,
            "domain": domain,
            "canonical_url": canonical_url,
            "extracted_text": full_text,
            "image_url": image_url,
            "paragraph_count": len(paragraphs)
        }
