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

from llama_index.core.ingestion import IngestionPipeline

from llama_index.core.extractors import TitleExtractor, SummaryExtractor

from llama_index.core.storage.docstore import SimpleDocumentStore

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore


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
    
CACHE_DIR='./pipeline_cache'
CHROMA_DIR = './chroma_db_cached'

def get_transformation():
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
        ),
        Settings.embed_model,
        TitleExtractor(),
        # SummaryExtractor()
    ]
    
def main():
    print('=' * 60)
    print('Ingestion pipeline with LlamaIndex Caching')
    print('=' * 60)
    
    #load documents
    print('\n[1/6] Loading documents...')
    
    documents = SimpleDirectoryReader(
        input_dir= './llamaindex-docs',
        required_exts=['.md'],
        num_files_limit=10
    ).load_data()
    
    print(f' Found {len(documents)} documents in source directory.')
    
    #created persistent chroma vectore store
    print('\n [2/6] Setting up ChromaDB vectore store...')
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection('llamaindex_docs')
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    print(f' ChromaDB path: {CHROMA_DIR}')
    print(f' Existing embeddings in ChromaDB: {chroma_collection.count()}')
    
    #create pipeline with docstore for deduplication
    print(f'\n [3/6] Creating iongestion pipeline with caching')
    pipeline = IngestionPipeline(
        transformations=get_transformation(),
        vector_store=vector_store,
        docstore=SimpleDocumentStore()
    )
    
    #Load existing cache if available
    if os.path.exists(CACHE_DIR):
        print(f'    Loading existing cache from {CACHE_DIR}...')
        pipeline.load(persist_dir=CACHE_DIR)
        print('     Cache loaded! Unchanged document will be skipped.')
    else:
        print('     No existing cache found. Will process all documents.')
        
    #run the pipeline - LlamaIndex will use cached tranformations
    print('\n [4/6] Running ingestion pipeline...')
    print('     (Cached tranformation will be reused - no redundant API calls)')
    
    import time
    start_time = time.time()
    processed_node = pipeline.run(documents= documents, show_progress=True)
    elapsed = time.time() - start_time
    
    #Report results
    print(f'\n      Pipeline completed in {elapsed:.2f} seconds.')
    print(f'        Nodes returned: {len(processed_node)}')
    print(f'        Total embeddings in ChromaDB: {chroma_collection.count()}')
    
    #Show metadata from firts processed node (if any)
    
    if processed_node:
        print('\n   Sample metada from first NEW node:')
        if processed_node[0].embedding:
            print(f'    -Embeddings dimensions: {len(processed_node[0].embedding)}')
        first_node_metada = processed_node[0].metadata
        for key, value in list(first_node_metada.items())[:3]:
            print(f'    - {key}:{value}')
            
    #persist cache for next run
    print(f'\n [5/6] Persisting cache to {CACHE_DIR}...')
    pipeline.persist(persist_dir=CACHE_DIR)
    print('     Chache saved! Next run will skip unchanged documents.')
    
    #Create index and query
    
    print('\n [6/6] Creating vector store index and testing query...')
    vector_index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = vector_index.as_query_engine()
    
    print('\n' + '=' * 60)
    print('Query test')
    print('=' * 60)
    query = 'What is LlamaIndex used for?'
    print(f'Query: {query}')
    response = query_engine.query(query)
    print(f'\nResponse: \n{response}')

if __name__ == '__main__':
    main()
    