from Pipeline import Pipeline

class PositionalIndex:
    """
    This class builds and manages a positional index for efficient proximity-based searching.
    It stores word positions in each document and allows retrieval based on term proximity.
    """
    def __init__(self):
        self.pipeline = Pipeline()
        self.positional_index = {}  # {term: {doc_id: [positions]}}
        self.all_docs = set()

    def build_index(self, file_path, doc_id):
        """Builds the positional index by processing and indexing tokens from a document."""
        stemmed_tokens = self.pipeline.process_text(file_path)
        self.all_docs.add(doc_id)

        # Store token positions for each document
        for position, token in enumerate(stemmed_tokens):
            if token not in self.positional_index:
                self.positional_index[token] = {}
            if doc_id not in self.positional_index[token]:
                self.positional_index[token][doc_id] = []
            
            self.positional_index[token][doc_id].append(position)

    def get_positions(self, term, doc_id):
        """Retrieves positions of a term in a given document."""
        stemmed_tokens = self.pipeline.process_query(term)
        if not stemmed_tokens:
            return []

        stemmed_term = stemmed_tokens[0]
        return self.positional_index.get(stemmed_term, {}).get(doc_id, [])

    def proximity_search(self, term1, term2, distance):
        """
        Finds documents where `term1` and `term2` appear within `distance` words of each other.
        Returns a set of matching document IDs.
        """
        stemmed_tokens1 = self.pipeline.process_query(term1)
        stemmed_tokens2 = self.pipeline.process_query(term2)

        if not stemmed_tokens1 or not stemmed_tokens2:
            return set()

        stemmed_term1, stemmed_term2 = stemmed_tokens1[0], stemmed_tokens2[0]

        # Check if both terms exist in the index
        if stemmed_term1 not in self.positional_index or stemmed_term2 not in self.positional_index:
            return set()

        # Find documents containing both terms
        docs1 = set(self.positional_index[stemmed_term1].keys())
        docs2 = set(self.positional_index[stemmed_term2].keys())
        common_docs = docs1 & docs2  # Intersection of document sets

        matching_docs = set()
        for doc_id in common_docs:
            positions1 = self.positional_index[stemmed_term1][doc_id]
            positions2 = self.positional_index[stemmed_term2][doc_id]

            # Check if any pair of positions satisfies the proximity condition
            for pos1 in positions1:
                for pos2 in positions2:
                    if abs(pos1 - pos2) <= int(distance):
                        matching_docs.add(doc_id)
                        break
                else:
                    continue
                break

        return matching_docs

    def get_all_docs(self):
        """Returns a set of all indexed document IDs."""
        return self.all_docs
