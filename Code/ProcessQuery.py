import re
from InvertedIndex import InvertedIndex
from PositionalIndex import PositionalIndex
import os
class QueryProcessor:
    

    def __init__(self, document_directory):

        self.inverted_index = InvertedIndex()
        self.positional_index = PositionalIndex()
        self.document_directory = document_directory
        self.document_names = {}  # Mapping of doc_id to document name

        for filename in os.listdir(document_directory):
            if filename.endswith('.txt'):
                match = re.match(r'(\d+)\.txt', filename)  # Extract number from filename
                if match:
                    doc_id = int(match.group(1))  # Convert extracted number to an integer
                    file_path = os.path.join(document_directory, filename)

                    self.inverted_index.build_index(file_path, doc_id)
                    self.positional_index.build_index(file_path, doc_id)
                    self.document_names[doc_id] = filename

        
    
    def get_document_names(self):
        """Return document names mapping"""
        return self.document_names
    
    def identify_query_type(self, query):
        """Identify if the query requires inverted index or positional index"""
        # Check for proximity queries (contains /)
        if '/' in query:
            return 'positional'
        
        # Check for boolean operators
        boolean_operators = ['AND', 'OR', 'NOT']
        for op in boolean_operators:
            if op in query:
                return 'inverted'
        
        # If it's a single word, use inverted index
        if len(query.split()) == 1:
            return 'inverted'
        
        # If none of the above, return invalid
        return 'invalid'
    
    def process_query(self, query):
        """Process a query and return matching documents"""
        query_type = self.identify_query_type(query)
        
        if query_type == 'invalid':
            return "Invalid query. Please use boolean operators (AND, OR, NOT) or proximity search (word1 word2 / distance)."
        
        if query_type == 'inverted':
            return self.process_boolean_query(query)
        
        if query_type == 'positional':
            return self.process_positional_query(query)
    
    def process_boolean_query(self, query):
        words = query.split()
        operators = {"AND", "OR"}
        stack = []  # To hold terms and intermediate results
        not_flag = False  # Tracks if NOT is applied to the next term

        for word in words:
            if word == "NOT":
                not_flag = True  # Mark the next term to be negated
            elif word in operators:
                stack.append(word)  # Push operator to stack
            else:
                # Fetch document set
                result = self.inverted_index.get_documents_with_term(word)
                
                # Apply NOT if needed
                if not_flag:
                    result = self.inverted_index.get_documents_without_term(word)
                    not_flag = False  # Reset NOT flag
                
                # Evaluate when operator is present in stack
                while stack and stack[-1] in operators:
                    operator = stack.pop()  # Pop the operator
                    left_operand = stack.pop()  # Pop the last evaluated result
                    if operator == "AND":
                        result = left_operand & result
                    elif operator == "OR":
                        result = left_operand | result
                
                # Push the evaluated result back to stack
                stack.append(result)

        # Final result should be the only element left in stack
        return stack[0] if stack else set()




        

    def process_positional_query(self, query):
        """Process a positional query using the positional index"""
        # Parse the query format: "term1 term2 / distance"
        pattern = r'(.*?)\s+(.*?)\s*/\s*(\d+)'
        match = re.match(pattern, query)
        print(match.groups())
        if match:
            term1, term2, distance = match.groups()
            results = self.positional_index.proximity_search(term1, term2, distance)
            return results
        
        return "Invalid proximity query. Format should be: word1 word2 / distance"