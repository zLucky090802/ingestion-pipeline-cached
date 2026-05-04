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
    
    
def main():
    documents =  SimpleDirectoryReader(
        input_dir='./llamaindex-docs',
        recursive=False,
        required_exts=['.md'],
        num_files_limit=20
    ).load_data()
    
 
    index = VectorStoreIndex.from_documents(
        documents,
        # node_parser = SentenceSplitter(),
    )
    
    #query the index
    
    query_engine = index.as_query_engine()
    response = query_engine.query('How to integrate pinecone as the vector database?')
    
    print(response)
    
    
if __name__ == '__main__':
    main()