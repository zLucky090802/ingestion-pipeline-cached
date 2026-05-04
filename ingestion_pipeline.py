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
    
PERSISTANCE_DIR='./pipeline:sotrage'
CHROMA_DIR = './chroma_db'

def get_transformation():
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
        ),
        Settings.embed_model,
        TitleExtractor(),
        SummaryExtractor()
    ]
    
def main():
    documents = SimpleDirectoryReader(
        input_dir= './llamaindex-docs',
        required_exts=['.md'],
        num_files_limit=10
    ).load_data()
    
    #created persistent chroma vectore store
    print('Setting up ChromaDB vectore store...')
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection('llamaindex_docs')
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    #check how many docs already in vector store
    existing_count = chroma_collection.count()
    print(f'ChromaDB already contains {existing_count} embeddings')
    
    if existing_count > 0:
        print('Using existing embeddings from chromaDB (skipping ingestion).')
    else:
        #Create anbd run the ingestion pipeline
        print('Creating ingestion pipeline...')
        
        pipeline = IngestionPipeline(
            transformations= get_transformation(),
            docstore=SimpleDocumentStore()
        )
        print('Running ingestion pipeline...')
        processed_nodes = pipeline.run(documents=documents)
    
        print(f'Processed into {len(processed_nodes)} nodes')
        
        
    print(f'Loaded {len(documents)} documents.')
    
    
    
    #chec if we have a persisttance cache to load
    if os.path.exists(PERSISTANCE_DIR):
        print('Loading persisted document store...')
        pipeline.docstore.load(persist_dir=PERSISTANCE_DIR)
        print('Loaded persisted document store.')
    
    
    #run the pipeline (will skip cached/unchanged documents)
    
    #persist the cache for the next run
    
    # print(f'Persisting document store... {PERSISTANCE_DIR}')
    # pipeline.docstore.persist(persist_dir=PERSISTANCE_DIR)
    #verify embeddings 
    if processed_nodes[0].embedding:
        print(f'Embedding dimensions: {len(processed_nodes[0].embedding)}')
        
    #extract and print metadata from the first node
    first_node_metadata = processed_nodes[0].metadata
    print('First node metada:')
    for key, value in first_node_metadata.items():
        print(f' {key}: {value}')
        
    #create the vector store index
    
    print('Creating vector store index...')
    vector_index = VectorStoreIndex(nodes=processed_nodes)
    print('Vector sotre index created.')
    
    #created query engine
    query_engine = vector_index.as_query_engine()
    #sample query
    response = query_engine.query('What is SimpleDirectoryReader?')
    
    print(response)
    
if __name__ == '__main__':
    main()