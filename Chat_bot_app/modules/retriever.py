def retrieve_context(collection, embed_model, query, k=5):
    query_embedding = embed_model.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return "\n\n".join(results["documents"][0])
