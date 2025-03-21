import re
import nltk
from nltk.stem import PorterStemmer

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)

class Pipeline:
    """
    A text processing pipeline that includes tokenization, stop-word removal, and stemming.
    """
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize_only(self, text):
        """
        Tokenize text by extracting words while converting to lowercase.
        Removes punctuation and special characters.
        """
        return re.findall(r'\w+', text.lower())
    
    def stemming(self, tokens):
        """
        Apply stemming to a list of tokens using Porter Stemmer.
        """
        return [self.stemmer.stem(word) for word in tokens]
        
    def process_text(self, file_path):
        """
        Process a text file: Tokenization, stop-word removal, and stemming.
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                text = file.read()
            
            # Load stop words
            with open("StopWords.txt", 'r', encoding='utf-8', errors='replace') as file:
                stop_words = set(file.read().splitlines())
            
            # Tokenize and stem
            tokens = self.tokenize_only(text)
            stemmed_tokens = self.stemming(tokens)

            # Remove stop words
            filtered_tokens = [word for word in stemmed_tokens if word not in stop_words]

            return filtered_tokens
        
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []

    def process_query(self, query_text):
        """
        Process a query string: Tokenization and stemming.
        """
        tokens = self.tokenize_only(query_text)
        return self.stemming(tokens)