import os
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader

#core data strcutures -- docs and settings
from llama_index.core import Document
from llama_index.core import Settings

#Text splitters
from llama_index.core.node_parser import SentenceSplitter

#embedding models

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#index creation - vectore stroe index
from llama_index.core import VectorStoreIndex

#llm configuration
from llama_index.llms.groq import Groq

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key
)
    
    
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512
Settings.chunk_overlap = 50
    
    
def main():
    
    documents = SimpleDirectoryReader(
        input_dir= './llamaindex-docs',
        required_exts=['.md'],
        num_files_limit=10
    ).load_data()
    
    print(f'Loaded {len(documents)} documents.')
    
    node_parser = SentenceSplitter(
        chunk_size=Settings.chunk_size,
        chunk_overlap=Settings.chunk_overlap
    )
    
    #parse documents into nodes with custom chunking
    print('Parsing documents into nodes with custom chuynking...')
    nodes = node_parser.get_nodes_from_documents(documents)
    print(f'Pased {len(nodes)} nodes from documents')
    
    #inspect a few sample nodes
    print('\nSample nodes after custom chunking')
    for i, node in enumerate(nodes[:3]):
        print(f'\nNode {i+1} content:\n{node.get_text()}\n')
        #Display metada if available
        if node.metadata:
            print(f' -source: {node.metadata.get('file_name','N/A')}')
            
    #create a vector store index from nodes
    print('Creating vectore index store from nodes...')
    
    index = VectorStoreIndex(nodes)
    print('Vector store index succesfully')
    
    query = 'What is llamaindex?'
    print(f'\nQuerying the index with: {query}')
    response = index.as_query_engine().query(query)
    print(f'Response: \n{response}')
            
    
if __name__ == '__main__':
    main()