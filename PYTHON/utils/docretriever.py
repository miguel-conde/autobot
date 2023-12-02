import dotenv
import openai
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, CSVLoader

dotenv.load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

class DocRetriever:
    """
    A class for retrieving and processing documents.

    Args:
        persist_directory (str): The directory to persist the vector database.
        docs_directory (str): The directory containing the documents.
        chunk_size (int, optional): The size of each text chunk. Defaults to 1000.
        chunk_overlap (int, optional): The overlap between text chunks. Defaults to 200.
        search_type (str, optional): The type of search algorithm to use. Defaults to 'mmr'.
        **loader_kwargs: Additional keyword arguments to be passed to the loader.

    Attributes:
        persist_directory (str): The directory to persist the vector database.
        docs_directory (str): The directory containing the documents.
        embedding (OpenAIEmbeddings): The embedding model for generating document embeddings.
        vectordb (Chroma): The vector database for storing document embeddings.
        retriever (Retriever): The retriever for searching and retrieving documents.

    Methods:
        None

    """

    def __init__(
            self, 
            persist_directory: str, 
            docs_directory: str, 
            chunk_size: int = 1000, 
            chunk_overlap: int = 200,
            search_type: str = 'mmr',
            k = 1,
            **loader_kwargs
            ) -> None:
        """
        Initialize the DocRetriever class.

        Args:
            persist_directory (str): The directory to persist the vector database.
            docs_directory (str): The directory containing the documents.
            chunk_size (int, optional): The size of each text chunk. Defaults to 1000.
            chunk_overlap (int, optional): The overlap between text chunks. Defaults to 200.
            search_type (str, optional): The type of search algorithm to use. Defaults to 'mmr'.
            **loader_kwargs: Additional keyword arguments to be passed to the loader.
        """
        
        self.persist_directory = persist_directory
        self.docs_directory = docs_directory

        # OpenAI embeddings
        self.embedding = OpenAIEmbeddings()

        if os.path.exists(persist_directory):
            # Load the persisted database from disk
            print("Loading existing Vector DB")
            self.vectordb = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embedding
                )
        else:
            print("Creating VectorDB")

            # Load text in docs
            loader = DirectoryLoader(
                docs_directory, 
                loader_cls=CSVLoader, 
                **loader_kwargs
            )
            doc = loader.load()

            # Splitting the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
                )
            texts = text_splitter.split_documents(doc)  # Added missing self.

            # Put the text chunks into embeddings in a local Chroma vector database.
            # Supplying a persist_directory will store the embeddings on the disk.
            self.vectordb = Chroma.from_documents(
                documents         = texts,
                embedding         = self.embedding,
                persist_directory = persist_directory
                )

            # Persist the db to disk
            self.vectordb.persist()

        # Create retriever
        self.retriever = self.vectordb.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k},
            )
