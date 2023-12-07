import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
import openai
import pickle


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

    def ask(self, question: str) -> str:
        if self.chain is None:
            response = "Por favor, añade un documento."
        else:
            response = self.chain({"question": question, "chat_history": self.chat_history, "file_name":self.filename})

            print(response)

            # Asegúrate de que la respuesta incluya la información del documento
            # file_name = response.get('file_name', 'Nombre del archivo no disponible')
            # response = response["answer"].strip()
            
            # self.chat_history.append((question, response))
            # # print(doc_info)
            # # # Añade la información del documento a la respuesta
            # # response += '\n\n' + doc_info
            # self.chat_history.append((question, response))
            # response += '\n\n' + file_name
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
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever())
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
            print("")
            # print(pickle.load(f))
            # self.chat_history = pickle.load(f)
        
