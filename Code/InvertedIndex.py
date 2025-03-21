from Pipeline import Pipeline

class InvertedIndex:
    def __init__(self):
        self.pipeline = Pipeline()
        self.inverted_index = {}
        self.all_docs = set()
    
    def build_index(self, file_path, doc_id):
        """Build an inverted index from document"""
        stemmed_tokens = self.pipeline.process_text(file_path)
        self.all_docs.add(doc_id)
        
        # Add each token to the inverted index
        for token in set(stemmed_tokens):  # Use set to count each term once per document
            if token not in self.inverted_index:
                self.inverted_index[token] = set()
            self.inverted_index[token].add(doc_id)
    
    def get_documents_with_term(self, term):
        """Get all documents containing a term"""
        stemmed_tokens = self.pipeline.process_query(term)
        if not stemmed_tokens:
            return set()
            
        stemmed_term = stemmed_tokens[0]
        return self.inverted_index.get(stemmed_term, set())
    
    def get_documents_without_term(self, term):
        """Get all documents that don't contain a term"""
        docs_with_term = self.get_documents_with_term(term)
        return self.all_docs - docs_with_term
    
    def boolean_AND(self, term1, term2):
        """Get documents containing both terms"""
        docs1 = self.get_documents_with_term(term1)
        docs2 = self.get_documents_with_term(term2)
        return docs1 & docs2
    
    def boolean_OR(self, term1, term2):
        """Get documents containing either term"""
        docs1 = self.get_documents_with_term(term1)
        docs2 = self.get_documents_with_term(term2)
        return docs1 | docs2
    
    def get_all_docs(self):
        """Return all document IDs"""
        return self.all_docs