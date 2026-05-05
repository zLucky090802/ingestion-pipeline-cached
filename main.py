import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, Settings

from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle


load_dotenv()

# Configuration
INDEX_NAME = "llamaindex-doc-helper"
api_key = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key
)
# LlamaIndex settings
Settings.llm = llm
Settings.embed_model = embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.chunk_size = 512
Settings.chunk_overlap = 50


@st.cache_resource
def get_index():
    """Connect to Pinecone vector store and return index."""
    print("Connecting to Pinecone vector store...")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    pinecone_index = pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index


def main():
   
    st.set_page_config(page_title='RAG with Pinecone Vectore Store', layout='wide')
    st.title('LlamaIndex Doc Helper with Pinecone Vectore Store')
    st.caption('Ask a question about your documents stored in Pinecone Vectore Store.')
    
    #Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'chat_engine' not in st.session_state:
        index = get_index()
        memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
        st.session_state.chat_engine = index.as_chat_engine(
            memory = memory,
            chat_mode=ChatMode.BEST,
            system_prompt = (
                "You are a helpful assistant that answers questions about LlamaIndex. "
                "Use the retrieved context to provide accurate, helpful answers. "
                "If you don't know the answer, say so."
            ),
        )
        
    #display chat messages from history
    
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    #chat input
    if prompt := st.chat_input('ask a question about your documents...'):
        #add user message to chat history
        st.session_state.messages.append({'role':'user', 'content':prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        #get response from the chat engine  
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                #update the las messages with the actual response
                response = st.session_state.chat_engine.chat(prompt)
                st.session_state.messages.append(
                    {'role':'assitant','content':response.response}
                )
                st.markdown(response.response)
        #add assistant response to chat history
        st.session_state.messages.append({'role':'assistant','content':response.response})
                
    # #debug handler
    # debug_handler = LlamaDebugHandler(print_trace_on_end=True)
    
    # #Create callback manager with handlers
    # callback_manager = CallbackManager(handlers=[debug_handler])
    
    # #attacht to settings object
    # Settings.callback_manager = callback_manager
    
    
    # index = get_index()
    # query = 'How do i use llamaindex with pinecone?'
    # query_engine = index.as_query_engine()
    # response = query_engine.query(query)
    # print(response)


if __name__ == "__main__":
    main()
