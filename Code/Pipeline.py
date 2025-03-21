import re
import nltk
from nltk.stem import PorterStemmer

nltk.download('punkt', quiet=True)

class Pipeline:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize_only(self, text):
        """Tokenize text without stemming"""
        tokens = re.findall(r'\w+', text.lower())
        return tokens
    
    def stemming(self, tokens):
        """Apply stemming to a list of tokens"""
        stemmed_tokens = [self.stemmer.stem(word) for word in tokens]
        return stemmed_tokens
        
    def process_text(self, file_path):
    
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
        
        with open("StopWords.txt",'r', encoding='utf-8', errors='replace') as file:
            stop_words = file.read().splitlines()
        
    
        #print(f"Raw text from {file_path}: {text[:200]}")  # Debugging

        tokens = self.tokenize_only(text)
        #print(f"Tokens: {tokens[:20]}")  # Debugging

        stemmed_tokens = self.stemming(tokens)
        for words in stemmed_tokens:
            if words in stop_words:
                stemmed_tokens.remove(words)

        
        #print(f"Stemmed Tokens: {stemmed_tokens[:20]}")  # Debugging

        return stemmed_tokens

    
    def process_query(self, query_text):
        """Process a query string"""
        tokens = self.tokenize_only(query_text)
        stemmed_tokens = self.stemming(tokens)
        return stemmed_tokens