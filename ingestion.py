from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import NodeParser
from llama_index.llms import groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import download_loader, ServiceContext, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone
import os

load_dotenv()
pc = pinecone(api_key=os.environ('PINECONE_API_KEY'))








if __name__ == '__main__':
    print('a')