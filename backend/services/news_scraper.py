"""Service for scraping news articles from Yahoo Finance and Google."""

import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urlparse, quote_plus


class NewsScraper:
    """Scraper for finding and extracting news articles."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.exclude_patterns = [
            'maps', 'policies', 'preferences', 'accounts', 'support',
            '/search', '/news/tagged/', 'calendar', 'screener', 'trending'
        ]

    def search_google(self, ticker: str, max_results: int = 10) -> List[str]:
        """
        Search Google for Yahoo Finance news URLs about a ticker.

        Args:
            ticker: Stock or crypto ticker symbol
            max_results: Maximum number of URLs to return

        Returns:
            List of news article URLs
        """
        search_url = f'https://www.google.com/search?q=yahoo+finance+{quote_plus(ticker)}&tbm=nws'

        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links
            links = []
            for link in soup.find_all('a', href=True):
                url = link['href']
                if 'url?q=' in url:
                    # Extract actual URL from Google redirect
                    url = url.split('url?q=')[1].split('&sa=U')[0]
                    if 'finance.yahoo.com' in url and self._is_valid_url(url):
                        links.append(url)
                        if len(links) >= max_results:
                            break

            return links[:max_results]

        except Exception as e:
            print(f"Error searching Google for {ticker}: {e}")
            return []

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is a valid news article (not a navigation page)."""
        for pattern in self.exclude_patterns:
            if pattern in url.lower():
                return False
        return True

    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape article content from a URL.

        Args:
            url: Article URL to scrape

        Returns:
            Dictionary with 'title', 'content', and 'url' or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title = None
            title_tag = soup.find('h1')
            if title_tag:
                title = title_tag.get_text().strip()

            # Extract article content
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs])

            # Limit content to ~350 words
            words = content.split()[:350]
            content = ' '.join(words)

            if content and len(content) > 100:
                return {
                    'url': url,
                    'title': title or 'No title',
                    'content': content
                }

            return None

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def scrape_ticker_news(self, ticker: str, max_articles: int = 10) -> List[Dict[str, str]]:
        """
        Find and scrape news articles for a ticker.

        Args:
            ticker: Stock or crypto ticker symbol
            max_articles: Maximum number of articles to scrape

        Returns:
            List of article dictionaries with 'title', 'content', and 'url'
        """
        urls = self.search_google(ticker, max_results=max_articles * 2)
        articles = []

        for url in urls:
            if len(articles) >= max_articles:
                break

            article = self.scrape_article(url)
            if article:
                articles.append(article)

        return articles
