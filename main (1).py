import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer

from llama_index.core.chat_engine.types import ChatMode

from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle


load_dotenv()

# Configuration
INDEX_NAME = "llamaindex-doc-helper"

# LlamaIndex settings
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 50


class DuplicateRemoverPostProcessor(BaseNodePostprocessor):
    """Post-processor to remove duplicate nodes based on text content."""

    similarity_threshold: float = 0.8  # Jaccard similarity threshold

    def _postprocess_nodes(
        self, nodes: list[NodeWithScore], query_bundle: QueryBundle = None
    ) -> list[NodeWithScore]:

        if not nodes:
            return nodes

        seen_texts = []
        unique_nodes = []

        for node in nodes:
            node_text = node.node.get_content()
            is_duplicate = False

            # Compare against all previously seen texts
            for seen_text in seen_texts:
                # Jaccard similarity
                node_words = set(node_text.lower().split())
                seen_words = set(seen_text.lower().split())

                overlap = len(node_words & seen_words)
                total = len(node_words | seen_words)
                jaccard_similarity = overlap / total if total > 0 else 0

                if jaccard_similarity > self.similarity_threshold:
                    is_duplicate = True
                    break

            # ✅ This must be OUTSIDE the inner for loop
            if not is_duplicate:
                unique_nodes.append(node)
                seen_texts.append(node_text)

        return unique_nodes


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
    st.set_page_config(
        page_title="RAG with Pinecone Vector Store", layout="wide", page_icon="📚"
    )
    st.title("LlamaIndex Doc Helper with Pinecone Vector Store")
    st.caption("Ask questions about your documents stored in Pinecone vector store.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize chat engine in session state
    if "chat_engine" not in st.session_state:
        index = get_index()
        memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

        # Create Sentence Embedding Optimizer post-processor
        sentence_optimizer = SentenceEmbeddingOptimizer(
            embed_model=Settings.embed_model,
            percentile_cutoff=0.5,  # keep top 50% sentences
            threshold_cutoff=0.7,  # minimum similarity score of 0.7
            context_before=1,  # include 1 sentence before
            context_after=1,
        )  # include 1 sentence after

        st.session_state.chat_engine = index.as_chat_engine(
            memory=memory,
            chat_mode=ChatMode.BEST,
            post_processors=[DuplicateRemoverPostProcessor(), sentence_optimizer],
            system_prompt=(
                "You are a helpful assistant that answers questions about LlamaIndex. "
                "Use the retrieved context to provide accurate, helpful answers. "
                "If you don't know the answer, say so."
            ),
        )

    # display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from chat engine
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # extract nodes from response
                response = st.session_state.chat_engine.chat(prompt)
                nodes = [node for node in response.source_nodes]
                # st.write(f"_Retrieved {len(nodes)} source documents._")

                if nodes:
                    with st.expander(f"📚 Retrieved {len(nodes)} source documents"):
                        for i, node in enumerate(nodes, 1):
                            score = node.score if node.score else "N/A"
                            source_file = node.metadata.get("file_name", "Unknown")

                            st.markdown(
                                f"**Source {i}** | Score: `{score:.4f}` | File: `{source_file}`"
                            )
                            st.markdown(
                                f"> {node.text[:500]}..."
                                if len(node.text) > 500
                                else f"> {node.text}"
                            )
                            st.divider()

            # Display the response
            st.markdown(response.response)

            # Extract and display source nodes (citations)
            nodes = [node for node in response.source_nodes]

            if nodes:
                with st.expander(f"📚 Sources ({len(nodes)} documents)"):
                    for i, node in enumerate(nodes, 1):
                        score = node.score if node.score else "N/A"
                        source_file = node.metadata.get("file_name", "Unknown")

                        st.markdown(
                            f"**Source {i}** | Score: `{score:.4f}` | File: `{source_file}`"
                        )
                        st.markdown(
                            f"> {node.text[:500]}..."
                            if len(node.text) > 500
                            else f"> {node.text}"
                        )
                        st.divider()

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response.response}
        )


if __name__ == "__main__":
    main()
