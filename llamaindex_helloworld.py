import os
from dotenv import load_dotenv 
from llama_index.llms.groq import Groq
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex, Settings

# IMPORTANTE: Importamos la clase explícita para los embeddings locales
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

def main():
    url = 'https://www.marca.com/'
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("Error: Revisa tu archivo .env, no se encontró GROQ_API_KEY")
        return

    # 1. Inicializamos Groq (El cerebro que lee y responde)
    llm = Groq(
        model="llama-3.1-8b-instant", 
        api_key=api_key
    )
    
    # 2. Inicializamos el modelo de embeddings EXPLÍCITAMENTE (El traductor matemático)
    # bge-small-en-v1.5 es excelente, rápido y pesa muy poco.
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # 3. Conectamos las piezas a la configuración global de LlamaIndex
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    print('Descargando la página web...')
    documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    print(f'Cargados {len(documents)} documento(s)\n')
    
    print('Creando el índice (descargando el modelo local y convirtiendo texto a vectores)...')
    # Nota: Esta línea tomará un poco de tiempo la primera vez porque descargará ~130MB a tu PC.
    index = VectorStoreIndex.from_documents(documents)
    print('¡Índice creado exitosamente!\n')
    
    query_engine = index.as_query_engine()
    
    query = 'What does Marca say about Vinicius?'
    print(f'Pregunta: {query}\n')
    
    response = query_engine.query(query)
    
    print(f'Respuesta:\n{response}\n')
  
if __name__ == "__main__":
    main()