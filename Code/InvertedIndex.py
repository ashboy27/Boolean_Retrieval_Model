from Pipeline import Pipeline

class InvertedIndex:
    def __init__(self):
        """Initialize the inverted index with a text processing pipeline."""
        self.pipeline = Pipeline()
        self.inverted_index = {}  # Dictionary to store term -> set(doc_ids)
        self.all_docs = set()  # Set to store all document IDs
    
    def build_index(self, file_path, doc_id):
        """Build an inverted index from a document."""
        stemmed_tokens = self.pipeline.process_text(file_path)
        self.all_docs.add(doc_id)
        
        for token in set(stemmed_tokens):  # Use a set to avoid redundant doc_id entries
            self.inverted_index.setdefault(token, set()).add(doc_id)
    
    def get_documents_with_term(self, term):
        """Retrieve documents that contain the given term."""
        stemmed_tokens = self.pipeline.process_query(term)
        if not stemmed_tokens:
            return set()
        
        return self.inverted_index.get(stemmed_tokens[0], set())
    
    def get_documents_without_term(self, term):
        """Retrieve documents that do not contain the given term."""
        return self.all_docs - self.get_documents_with_term(term)
    
    def boolean_AND(self, term1, term2):
        """Retrieve documents containing both terms (AND operation)."""
        return self.get_documents_with_term(term1) & self.get_documents_with_term(term2)
    
    def boolean_OR(self, term1, term2):
        """Retrieve documents containing either term (OR operation)."""
        return self.get_documents_with_term(term1) | self.get_documents_with_term(term2)
    
    def get_all_docs(self):
        """Return the set of all document IDs."""
        return self.all_docs
