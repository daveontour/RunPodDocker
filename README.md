# RunPod Ollama Worker (native Ollama API)

This project runs an Ollama-backed RunPod Serverless worker using native Ollama endpoints (`/api/generate`, `/api/embed`, `/api/chat`, `/api/tags`).

The project used [https://github.com/svenbrnn/runpod-worker-ollama](https://github.com/svenbrnn/runpod-worker-ollama) as an example of how to implement for Docker

## What this worker supports

- Text generation via `prompt`
- Model listing via `list_models: true`
- Embeddings via `embeddingRequest`
- Image classification/question chat via image base64 requests

## Run locally

From the repository root:

```bash
python src/handler.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_api_port 8000
```

Or use the container entrypoint script in `src/start.sh`, which starts Ollama, pulls required models, and runs the API server.

## Example requests

Use `POST /runsync` with one of the following payload shapes:

- Prompt:
```json
{"input":{"prompt":"How are you?"}}
```
- List models:
```json
{"input":{"list_models":true}}
```
- Embeddings:
```json
{"input":{"embeddingRequest":"<The text to create the embedding from>"}}
```
- Image Classification:
```json
{"input":{"imageClassifyRequest":"<base64 encoded image>"}}
```
- Image Content Query:
```json
{"input":{
    "imageQuestionRequest":"<base64 encoded image>",
    "question":"<Any question related to the contents of the encoded image>"
    }}
```

## Environment variables

| Variable Name | Description | Default Value |
|---|---|---|
| `OLLAMA_BASE_URL` | Base URL for Ollama API | `http://127.0.0.1:11434` |
| `MAX_CONCURRENCY` | RunPod concurrency modifier | `8` |

## Licence

This project is licensed under the Creative Commons Attribution 4.0 International License. You are free to use, share, and adapt the material for any purpose, even commercially, under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, see the [license](https://creativecommons.org/licenses/by/4.0/).