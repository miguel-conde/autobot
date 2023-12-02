import os
from utils.docretriever import DocRetriever

class TestDocRetriever:
    def setup_method(self):
        self.persist_directory = "test_data/persist"
        self.docs_directory = "test_data/docs"
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.search_type = 'mmr'
        self.loader_kwargs = {}

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
        invalid_directory = "invalid_directory"
        retriever = DocRetriever(
            invalid_directory,
            self.docs_directory,
            self.chunk_size,
            self.chunk_overlap,
            self.search_type,
            **self.loader_kwargs
        )
        assert retriever.persist_directory == invalid_directory
        assert retriever.docs_directory == self.docs_directory
        assert retriever.embedding is not None
        assert retriever.vectordb is not None
        assert retriever.retriever is not None
