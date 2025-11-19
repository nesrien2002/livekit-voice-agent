"""
RAG System for Knowledge Base Retrieval
Uses FAISS for vector similarity search and sentence-transformers for embeddings
"""

import os
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss
import pickle


class RAGSystem:
    """Retrieval-Augmented Generation system for context retrieval"""

    def __init__(self, knowledge_base_path: str = "knowledge_base",
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG system

        Args:
            knowledge_base_path: Path to directory containing knowledge base documents
            model_name: Name of the sentence-transformer model to use
        """
        print("Initializing RAG System...")

        # Load embedding model
        print(f"Loading embedding model: {model_name}")
        self.embedder = SentenceTransformer(model_name)

        # Load documents
        self.documents = []
        self.document_metadata = []
        self.load_documents(knowledge_base_path)

        # Create embeddings and FAISS index
        print("Creating document embeddings...")
        self.create_index()

        print(f"RAG System initialized with {len(self.documents)} documents")

    def load_documents(self, path: str) -> None:
        """
        Load all text documents from the knowledge base directory

        Args:
            path: Path to knowledge base directory
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Knowledge base path not found: {path}")

        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                filepath = os.path.join(path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Split into chunks (by paragraph or section)
                    chunks = self.split_into_chunks(content)

                    for i, chunk in enumerate(chunks):
                        self.documents.append(chunk)
                        self.document_metadata.append({
                            'source': filename,
                            'chunk_id': i
                        })

        print(f"Loaded {len(self.documents)} document chunks from {path}")

    def split_into_chunks(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """
        Split text into smaller chunks for better retrieval

        Args:
            text: Input text to split
            max_chunk_size: Maximum characters per chunk

        Returns:
            List of text chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks if chunks else [text]

    def create_index(self) -> None:
        """Create FAISS index from document embeddings"""
        if not self.documents:
            raise ValueError("No documents loaded")

        # Generate embeddings for all documents
        self.embeddings = self.embedder.encode(
            self.documents,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.index.add(self.embeddings.astype('float32'))

        print(f"FAISS index created with {self.index.ntotal} vectors")

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float, dict]]:
        """
        Retrieve the most relevant documents for a query

        Args:
            query: User query string
            top_k: Number of top documents to retrieve

        Returns:
            List of tuples (document_text, similarity_score, metadata)
        """
        # Embed the query
        query_embedding = self.embedder.encode(
            [query],
            convert_to_numpy=True
        ).astype('float32')

        # Search in FAISS index
        distances, indices = self.index.search(query_embedding, top_k)

        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):  # Valid index
                results.append((
                    self.documents[idx],
                    float(distances[0][i]),
                    self.document_metadata[idx]
                ))

        return results

    def get_context_string(self, query: str, top_k: int = 3) -> str:
        """
        Get a formatted context string for a query

        Args:
            query: User query
            top_k: Number of documents to retrieve

        Returns:
            Formatted context string
        """
        results = self.retrieve(query, top_k)

        if not results:
            return "No relevant information found in knowledge base."

        context_parts = []
        for i, (doc, score, metadata) in enumerate(results, 1):
            context_parts.append(f"[Source {i}: {metadata['source']}]\n{doc}\n")

        return "\n".join(context_parts)

    def save_index(self, filepath: str = "rag_index.pkl") -> None:
        """Save the RAG index to disk"""
        data = {
            'documents': self.documents,
            'metadata': self.document_metadata,
            'embeddings': self.embeddings
        }

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        # Save FAISS index separately
        faiss.write_index(self.index, filepath + ".faiss")
        print(f"Index saved to {filepath}")

    def load_index(self, filepath: str = "rag_index.pkl") -> None:
        """Load the RAG index from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.documents = data['documents']
        self.document_metadata = data['metadata']
        self.embeddings = data['embeddings']

        # Load FAISS index
        self.index = faiss.read_index(filepath + ".faiss")
        print(f"Index loaded from {filepath}")


# Test the RAG system
if __name__ == "__main__":
    # Initialize RAG system
    rag = RAGSystem()

    # Test queries
    test_queries = [
        "What are your business hours?",
        "How do I reset my password?",
        "What are the pricing plans?",
        "How do I authenticate with the API?"
    ]

    print("\n" + "=" * 60)
    print("Testing RAG System")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)

        results = rag.retrieve(query, top_k=2)

        for i, (doc, score, metadata) in enumerate(results, 1):
            print(f"\nResult {i} (Score: {score:.4f}):")
            print(f"Source: {metadata['source']}")
            print(f"Content: {doc[:200]}...")