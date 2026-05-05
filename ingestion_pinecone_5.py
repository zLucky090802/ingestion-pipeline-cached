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
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

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

INDEX_NAME = 'llamaindex-doc-helper'
EMBEDDING_DIMENSION = 384

def get_transformation():
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
        ),
        Settings.embed_model,
        # TitleExtractor(),
        # SummaryExtractor()
    ]
    
def main():
    print('=' * 60)
    print('Ingestion pipeline with LlamaIndex Caching')
    print('=' * 60)
    
    
    #connect to pinecone vector store
    print('Connecting to pinecone vector store...')
    pc = Pinecone(
        api_key=os.getenv('PINECONE_API_KEY')
    )
    
    pinecone_index = pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    #check current stast
    
    stast = pinecone_index.describe_index_stats()
    
    print(f'        Connected to index: {INDEX_NAME}')
    print(f'        Current vector in index: {stast.total_vector_count}')
    
    #load all documents from the data directorey
    print('Loading documents from data directory...')
    documents = SimpleDirectoryReader(
        input_dir= './llamaindex-docs',
        required_exts=['.md'],
       
    ).load_data()
    
    print(f'    Loaded {len(documents)} documents')
    
    print(f'\n Creating iongestion pipeline with caching')
    pipeline = IngestionPipeline(
        transformations=get_transformation(),
        vector_store=vector_store,
        docstore=SimpleDocumentStore()
    )
    
    
    print('\n [4/6] Running ingestion pipeline...')
    print('     (Cached tranformation will be reused - no redundant API calls)')
    
    import time
    start_time = time.time()
    processed_node = pipeline.run(documents= documents, show_progress=True, num_workers=4)
    elapsed = time.time() - start_time
    
    #Report results
    print(f'\n      Pipeline completed in {elapsed:.2f} seconds.')
    print(f'        Nodes returned: {len(processed_node)}')

    #testing and verify query
    
    print('\n testing query...')
    stast = pinecone_index.describe_index_stats()
    print(f'        Total vectors in pinecone: {stast.total_vector_count}')
    
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()
    
    response = query_engine.query('what is llamaindex?')
    
    print(f'\n       Query response: {response}')

if __name__ == '__main__':
    main()
    