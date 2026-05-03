#!/bin/bash

cleanup() {
    echo "Cleaning up..."
    pkill -P $$ # Kill all child processes of the current script
    exit 0
}

# Trap exit signals and call the cleanup function
trap cleanup SIGINT SIGTERM

# Kill any existing ollama processes
pgrep ollama | xargs kill

# verify volume is mounted
echo "Volume is mounted: $(ls -la /runpod-volume/models)"
print(os.listdir('/runpod-volume'))


# Start the ollama server and log its output
ollama serve 2>&1 | tee ollama.server.log &
OLLAMA_PID=$! # Store the process ID (PID) of the background command

check_server_is_running() {
    echo "Checking if server is running..."
    if cat ollama.server.log | grep -q "Listening"; then
        return 0 # Success
    else
        return 1 # Failure
    fi
}

# Wait for the server to start
while ! check_server_is_running; do
    sleep 5
done

# ollama pull gemma4:latest
# ollama pull embeddinggemma:latest

python -u handler.py $1
#python -u handler.py "${1:---rp_serve_api}" --rp_api_host 0.0.0.0 --rp_api_port 8000