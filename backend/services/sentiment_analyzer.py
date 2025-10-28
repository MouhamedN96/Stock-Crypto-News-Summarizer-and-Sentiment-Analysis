"""Service for analyzing sentiment of text using transformers."""

from transformers import pipeline
from typing import List, Dict, Optional


class SentimentAnalyzer:
    """Analyzer for sentiment classification of financial text."""

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize sentiment analyzer.

        Args:
            model_name: Optional specific model name, defaults to transformers default
        """
        self.model_name = model_name
        self.pipeline = None

    def load_model(self):
        """Load the sentiment analysis pipeline."""
        if self.pipeline is None:
            print("Loading sentiment analysis model")
            if self.model_name:
                self.pipeline = pipeline('sentiment-analysis', model=self.model_name)
            else:
                self.pipeline = pipeline('sentiment-analysis')
            print("Sentiment model loaded")

    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with 'label' and 'score'
        """
        if self.pipeline is None:
            self.load_model()

        try:
            # Truncate text if too long (max 512 tokens for most models)
            text = text[:2000]
            result = self.pipeline(text)[0]

            return {
                'label': result['label'],
                'score': round(result['score'], 4)
            }

        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                'label': 'UNKNOWN',
                'score': 0.0
            }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Analyze sentiment of multiple texts.

        Args:
            texts: List of texts to analyze

        Returns:
            List of dictionaries with 'label' and 'score'
        """
        if self.pipeline is None:
            self.load_model()

        results = []
        for text in texts:
            result = self.analyze(text)
            results.append(result)

        return results

    def unload_model(self):
        """Unload model from memory."""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
            print("Sentiment model unloaded")
