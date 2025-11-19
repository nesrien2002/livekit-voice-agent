from rag_system import RAGSystem

# Initialize RAG
rag = RAGSystem()

# Test query
query = "What are your business hours?"
results = rag.retrieve(query)

print("Query:", query)
print("\nRetrieved documents:")
for i, doc in enumerate(results, 1):
    print(f"\n{i}. {doc[:200]}...")  # Print first 200 chars