from transformers import BartForConditionalGeneration, BartTokenizer
# BartForConditionalGeneration, BartTokenizer - Hugging face's pre-trained BART model for summarization
import requests # fetch webpage content
from bs4 import BeautifulSoup # parse and clean HTML content from URLs

class TextSummarizer:
    def __init__(self):
        # Load pre-trained BART model and tokenizer
        self.model_name = "facebook/bart-large-cnn"
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name)

    def summarize_text(self, text, summary_length="medium"):
        # Takes a text input 
        length_map = {
            "short": 50,
            "medium": 100,
            "long": 200
        }
        max_length = length_map.get(summary_length, 100)
        min_length = max_length // 2

        # Tokenize input into tensors
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

        # Generate summary
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,  # tries 4 sequences and pick the best
            early_stopping=True
        )

        # Decode summary tensor into text
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def extract_text_from_url(self, url):
        try:
            # Fetch webpage content
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse HTML and extract text
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove script and style content
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract text from paragraphs, headings, and articles
            text_elements = soup.find_all(["p", "h1", "h2", "h3", "article"])
            text = " ".join([element.get_text(strip=True) for element in text_elements])

            # Clean up text (remove excessive whitespace)
            text = " ".join(text.split())
            return text if text else "Error: No text found on the webpage."
        except Exception as e:
            return f"Error fetching URL: {str(e)}"
    
