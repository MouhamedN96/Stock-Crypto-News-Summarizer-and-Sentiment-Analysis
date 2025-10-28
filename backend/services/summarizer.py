"""Service for summarizing news articles using Pegasus model."""

from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from typing import List, Optional
import torch


class NewsSummarizer:
    """Summarizer using financial-summarization-pegasus model."""

    def __init__(self, model_name: str = "human-centered-summarization/financial-summarization-pegasus"):
        """
        Initialize the summarizer with Pegasus model.

        Args:
            model_name: HuggingFace model name for summarization
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """Load the tokenizer and model."""
        if self.model is None:
            print(f"Loading summarization model: {self.model_name}")
            self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
            self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
            self.model = self.model.to(self.device)
            print(f"Model loaded on device: {self.device}")

    def summarize(self, text: str, max_length: int = 55, min_length: int = 20) -> Optional[str]:
        """
        Summarize a single text.

        Args:
            text: Text to summarize
            max_length: Maximum length of summary in tokens
            min_length: Minimum length of summary in tokens

        Returns:
            Summary text or None if failed
        """
        if self.model is None:
            self.load_model()

        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                max_length=512,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)

            # Generate summary
            summary_ids = self.model.generate(
                inputs['input_ids'],
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )

            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary

        except Exception as e:
            print(f"Error summarizing text: {e}")
            return None

    def summarize_batch(self, texts: List[str], max_length: int = 55) -> List[str]:
        """
        Summarize multiple texts.

        Args:
            texts: List of texts to summarize
            max_length: Maximum length of summary in tokens

        Returns:
            List of summaries
        """
        summaries = []
        for text in texts:
            summary = self.summarize(text, max_length=max_length)
            summaries.append(summary if summary else "")

        return summaries

    def unload_model(self):
        """Unload model from memory to free resources."""
        if self.model is not None:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            print("Model unloaded from memory")
