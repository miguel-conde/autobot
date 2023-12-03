import os
import pytest
from utils.docretriever import DocRetriever
from utils import globalsettings as gs  

class TestDocRetriever:
    def setup_method(self):
        self.persist_directory = gs.the_folders.VECTORSTORE
        self.docs_directory = gs.the_folders.MMM_DOCS
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.search_type = 'mmr'
        self.loader_kwargs = {'encoding': 'utf-8', 'csv_args': {'delimiter': ';'}}

    def teardown_method(self):
        if os.path.exists(self.persist_directory):
            os.remove(self.persist_directory)


        retriever = DocRetriever(
            self.persist_directory,
            self.docs_directory,
            self.chunk_size,
            self.chunk_overlap,
            self.search_type,
            **self.loader_kwargs
        )
        assert retriever.persist_directory == self.persist_directory
        assert retriever.docs_directory == self.docs_directory
        assert retriever.embedding is not None
        assert retriever.vectordb is not None
        assert retriever.retriever is not None

    def test_init_existing_db(self):
        os.makedirs(self.persist_directory, exist_ok=True)
        retriever = DocRetriever(
            self.persist_directory,
            self.docs_directory,
            self.chunk_size,
            self.chunk_overlap,
            self.search_type,
            **self.loader_kwargs
        )
        assert retriever.persist_directory == self.persist_directory
        assert retriever.docs_directory == self.docs_directory
        assert retriever.embedding is not None
        assert retriever.vectordb is not None
        assert retriever.retriever is not None

    def test_init_invalid_db(self):
        # Definir un directorio que no existe
        nonexistent_directory = "/nonexistent/directory"
    
        # Verificar que se produce una excepción al intentar inicializar con un directorio inexistente
        with pytest.raises(Exception):
            retriever = DocRetriever(
                nonexistent_directory,
                nonexistent_directory,
                self.chunk_size,
                self.chunk_overlap,
                self.search_type,
                **self.loader_kwargs
            )


