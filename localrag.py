import torch
import ollama
import os
import argparse

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the input query
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=user_input)["embedding"]
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    # Sort the scores and get the top-k indices
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def run_without_rag(user_query, model):
    """Generate response without RAG (direct LLM query)."""
    response = ollama.generate(model=model, prompt=user_query)
    print(NEON_GREEN + "Response without RAG:\n" + RESET_COLOR)
    print(response['response'])

def run_with_rag(user_query, vault_embeddings, vault_content, model):
    """Generate response with RAG (using external context)."""
    relevant_context = get_relevant_context(user_query, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print(CYAN + "Context pulled from documents:\n" + RESET_COLOR + context_str)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)
        context_str = ""

    user_query_with_context = f"{context_str}\n\n{user_query}" if context_str else user_query

    response = ollama.generate(model=model, prompt=user_query_with_context)
    print(NEON_GREEN + "Response with RAG:\n" + RESET_COLOR)
    print(response['response'])

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Ollama Chat with or without RAG")
    parser.add_argument("--mode", choices=["rag", "no-rag"], default="no-rag", help="Choose between 'rag' or 'no-rag' mode.")
    parser.add_argument("--model", default="llama2", help="Ollama model to use (default: mistral).")
    #parser.add_argument("--temperature", type=float, default=0.7, help="Set the model's creativity level (0.0 - 1.0).")
    args = parser.parse_args()

    # Load the vault content
    print(NEON_GREEN + "Loading vault content..." + RESET_COLOR)
    vault_content = []
    if os.path.exists("vault.txt"):
        with open("vault.txt", "r", encoding="utf-8") as vault_file:
            vault_content = vault_file.readlines()

    # Generate embeddings for the vault content
    print(NEON_GREEN + "Generating embeddings for the vault content..." + RESET_COLOR)
    vault_embeddings = []
    for content in vault_content:
        response = ollama.embeddings(model="mxbai-embed-large", prompt=content)
        vault_embeddings.append(response["embedding"])
    vault_embeddings_tensor = torch.tensor(vault_embeddings)

    print(NEON_GREEN + "Starting conversation loop..." + RESET_COLOR)

    while True:
        user_query = input(YELLOW + "Ask a query about your documents (or type 'quit' to exit): " + RESET_COLOR)
        if user_query.lower() == "quit":
            break

        if args.mode == "rag":
            run_with_rag(user_query, vault_embeddings_tensor, vault_content, args.model)
        else:
            run_without_rag(user_query, args.model)

if __name__ == "__main__":
    main()
