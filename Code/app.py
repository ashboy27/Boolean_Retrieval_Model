import streamlit as st
import os
from ProcessQuery import QueryProcessor

def runapp(DocumentFolder:str):
    st.title("Information Retrieval System")
    
    # Initialize session state for query processor if not exists
    if 'query_processor' not in st.session_state:
        # Set the documents directory
        doc_dir = os.path.join(os.getcwd(),DocumentFolder)  
        # Initialize QueryProcessor
        st.session_state.query_processor = QueryProcessor(doc_dir)
        st.session_state.doc_names = st.session_state.query_processor.get_document_names()
    
    # Search box
    query = st.text_input("Enter your search query:", 
                          help="Use boolean operators (AND, OR, NOT) or proximity search (word1 word2 / distance)")

    # Search button
    if st.button("Search") or query:
        if query:
            with st.spinner("Searching..."):
                result = st.session_state.query_processor.process_query(query)
                if isinstance(result, str):  # Error message
                    st.error(result)
                
                

                
                else:  # Document list
                    st.success(f"Found {len(result)} matching documents")
                    result = sorted(list(result))
                    if result:
                        st.subheader("Matching Documents:")
                        for doc_id in result:
                            doc_name = st.session_state.doc_names.get(str(doc_id), f"{doc_id}")


                            if not doc_name.endswith(".txt"):
                                doc_name += ".txt"

                            with st.expander(f"{doc_name}"):
                                try:
                                    # Use correct document directory
                                    file_path = os.path.join(st.session_state.query_processor.document_directory, doc_name)
                                    #print(f"DEBUG: Trying to open {file_path}")  # Debugging output

                                    with open(file_path, 'r', encoding="utf-8") as f:
                                        content = f.read()
                                    st.text(content[:500] + "..." if len(content) > 500 else content)
                                except Exception as e:
                                    st.write(f"Unable to display document content. Error: {str(e)}")
                    else:
                        st.info("No matching documents found")

    # Query examples
    st.sidebar.header("Query Examples")
    st.sidebar.markdown("""
    **Boolean Queries:**
    - `information`
    - `information AND retrieval`
    - `information OR retrieval`
    - `NOT information`
    
    **Proximity Queries:**
    - `information retrieval / 3` (finds documents where 'information' and 'retrieval' appear within 3 words of each other)
    """)



