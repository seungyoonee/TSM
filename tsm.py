from tsm_model import TSMModel

def main():
    # Initialize model
    tsm = TSMModel("seungyoonee/tsm-contriever")

    # Example query
    query = "Who won the world cup in 2022?"
    
    # List of documents
    documents = [
        "Argentina won the World Cup in 2022.",
        "France won the World Cup in 2018.",
        "Argentina won the Copa America in 2021.",
        "Rafael Nadal won the French Open in 2022.",
        "The weather is nice today."
    ]
    
    print(f"Query: {query}\n")
    
    for doc in documents:
        score = tsm.compute_score(query, doc)
        print(f"Document: {doc}")
        print(f"Score: {score:.4f}\n")

if __name__ == "__main__":
    main()
