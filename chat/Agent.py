import os
#from docx import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
import openai
import pickle
from langchain_core.documents.base import Document as Doc

class Agent:
    def __init__(self, openai_api_key: str = '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'):
        # if openai_api_key is None, then it will look the enviroment variable OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chat_history = None
        self.chain = None
        self.db = None
        self.filename = None
        self.metadata = None
        # self.memory = VectorStoreRetrieverMemory(retriever=self.embeddings, memory_key="chat_history", return_docs=False, return_messages=True)

    def ask(self, question: str) -> str:
        # Inicializa la respuesta con un mensaje por defecto
        if self.chain is None:
            response = "Por favor, añade un documento."
        else:
            # Intenta obtener una respuesta de la cadena
            try:

                chat_history_tuples = []
                file_name = ''
                metadata = []
                model = 'gpt-3.5-turbo'
                response = self.chain({"question": question, "model":model, "chat_history": chat_history_tuples, "metadata": metadata})
                
                self.chat_history.append((question, response))
                # print(type(response))
                source_documents = response.get('source_documents', [])
                # print(type(source_documents))
                response = response["answer"].strip()

                # Busca el documento de origen en los documentos fuente
                for doc in source_documents:
                    # print(type(doc))
                    # doc = tuple
                    if isinstance(doc, Doc):
                        metadata = doc.metadata
                        if 'file_name' in metadata:
                            
                            file_name = metadata['file_name']
                            page = str(metadata['page'])
                            
                            file_name = ' (' + file_name + '.pdf'
                            page = ' - pag.' + page + ')'
                            # page = ' - ' + page + '.)'
                response += '\n\n' + file_name + page
            except Exception as e:
                # Si algo va mal, actualiza la respuesta con un mensaje de error
                response = f"Se produjo un error al procesar la pregunta:  {str(e)}"
        return response

    def ingest(self, file_path: os.PathLike, filename: str) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        for doc in documents:
            doc.metadata['file_name'] = os.path.basename(filename)
        splitted_documents = self.text_splitter.split_documents(documents)

        # Imprime el contenido de splitted_documents antes de guardar el archivo pickle
        # print("splitted_documents:", splitted_documents)

        if self.db is None:
            self.db = FAISS.from_documents(splitted_documents, self.embeddings)
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever(), return_source_documents=True,)
            if self.chat_history is None:
                self.chat_history = []
            else:
                self.chat_history.extend(splitted_documents)
        else:
            self.db.add_documents(splitted_documents)
        
        # Guarda los documentos en el disco
        with open('db.pkl', 'wb') as f:
            pickle.dump(splitted_documents, f)


    def load(self) -> None:
        """
        Carga el historial de chat desde un archivo pickle.
        """
        with open('db.pkl', 'rb') as f:
            try:
                self.chat_history = pickle.load(f)
                if self.chain is None and self.chat_history:
                    self.db = FAISS.from_documents(self.chat_history, self.embeddings)
                    self.chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever(), return_source_documents=True,)
            except EOFError:
                print("El archivo está vacío.")
                self.chat_history = []
