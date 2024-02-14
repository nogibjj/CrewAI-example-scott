#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Wait for the server to start up
sleep 10 # Adjust the sleep time as necessary     

# Download and set up the LLM (e.g., llama2)
ollama run llama2 &
ollama run mistral &
ollama run codellama 
# ollama pull solar &
# ollama pull openhermes & 
# Keep the script running to prevent the container from exiting
wait
