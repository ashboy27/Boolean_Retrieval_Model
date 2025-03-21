import re
import os
from InvertedIndex import InvertedIndex
from PositionalIndex import PositionalIndex

class QueryProcessor:
    """
    Handles query processing for both Boolean and Proximity search using Inverted and Positional Indexes.
    """
    
    def __init__(self, document_directory):
        """
        Initializes the query processor by building the indexes from the given document directory.
        """
        self.inverted_index = InvertedIndex()
        self.positional_index = PositionalIndex()
        self.document_directory = document_directory
        self.document_names = {}  # Mapping of doc_id to document name

        # Build indices from document directory
        for filename in os.listdir(document_directory):
            if filename.endswith('.txt'):
                match = re.match(r'(\d+)\.txt', filename)  # Extract numeric doc_id from filename
                if match:
                    doc_id = int(match.group(1))
                    file_path = os.path.join(document_directory, filename)
                    self.inverted_index.build_index(file_path, doc_id)
                    self.positional_index.build_index(file_path, doc_id)
                    self.document_names[doc_id] = filename
    
    def get_document_names(self):
        """Returns the mapping of document IDs to document names."""
        return self.document_names
    
    def identify_query_type(self, query):
        """Identifies if the query is Boolean or Positional."""
        if '/' in query:
            return 'positional'  # Proximity search
        
        boolean_operators = {'AND', 'OR', 'NOT'}
        for op in boolean_operators:
            if op in query:
                return 'inverted'  # Boolean search
        
        return 'inverted' if len(query.split()) == 1 else 'invalid'
    
    def process_query(self, query):
        """Processes a given query and returns matching document IDs."""
        query_type = self.identify_query_type(query)
        
        if query_type == 'invalid':
            return "Invalid query. Please use boolean operators (AND, OR, NOT) or proximity search (word1 word2 / distance)."
        
        return self.process_boolean_query(query) if query_type == 'inverted' else self.process_positional_query(query)
    
    def process_boolean_query(self, query):
        """Processes a Boolean query using the inverted index."""
        words = query.split()
        operators = {"AND", "OR"}
        stack = []  # Stack to hold terms and intermediate results
        not_flag = False  # Tracks if NOT is applied to the next term

        for word in words:
            if word == "NOT":
                not_flag = True  # Mark next term for negation
            elif word in operators:
                stack.append(word)  # Push operator onto stack
            else:
                result = self.inverted_index.get_documents_with_term(word)
                
                if not_flag:
                    result = self.inverted_index.get_documents_without_term(word)
                    not_flag = False  # Reset NOT flag
                
                # Process stacked operators
                while stack and stack[-1] in operators:
                    operator = stack.pop()
                    left_operand = stack.pop()
                    result = left_operand & result if operator == "AND" else left_operand | result
                
                stack.append(result)  # Push evaluated result back to stack

        return stack[0] if stack else set()
    
    def process_positional_query(self, query):
        """Processes a proximity search query using the positional index."""
        pattern = r'(.*?)\s+(.*?)\s*/\s*(\d+)'
        match = re.match(pattern, query)
        
        if match:
            term1, term2, distance = match.groups()
            return self.positional_index.proximity_search(term1, term2, int(distance))
        
        return "Invalid proximity query. Format should be: word1 word2 / distance"
