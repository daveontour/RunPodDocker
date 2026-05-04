import os
import base64

import httpx
from utils import JobInput


def _ollama_base_url() -> str:
    base = os.environ.get("OLLAMA_BASE_URL", "").strip().rstrip("/")
    if not base:
        base = "http://127.0.0.1:11434"
    return base


class OllamaEngine:
    def __init__(self):
        print ("OllamaEngine initialized")

    async def generate(self, job_input):
        model =  "gemma4:e4b"
        embedding_model = "embeddinggemma:latest"

        if job_input.list_models:
            url = f"{_ollama_base_url()}/api/tags"
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        yield {"error": f"HTTP {resp.status_code}: {resp.text}"}
                        return
                    yield resp.json()
            except httpx.RequestError as e:
                yield {"error": str(e)}
            return

        if job_input.volume_content:
            path = "/runpod-volume"
            content = os.listdir(path)
            body = {"content": content}
            yield body
            return

        if job_input.prompt:
            path = "/api/generate"
            body = {"model": model, "prompt": job_input.prompt, "stream": False}
        elif job_input.embeddingRequest:
            path = "/api/embed"
            body = {"model": embedding_model, "input": job_input.embeddingRequest}
        elif job_input.imageClassifyRequest:
            raw = job_input.imageClassifyRequest           
            if not isinstance(raw, str) or not raw.strip():
                yield {"error": "imageClassifyRequest must be a non-empty base64 image string"}
                return
            path = "/api/chat"
            body = self._image_classification_body(raw.strip(), model)
        elif job_input.imageQuestionRequest:
            raw = job_input.imageQuestionRequest           
            if not isinstance(raw, str) or not raw.strip():
                yield {"error": "imageClassifyRequest must be a non-empty base64 image string"}
                return
            path = "/api/chat"
            body = self._image_question_body(raw.strip(), job_input.question, model)
        else:
            yield {"error": "Missing or invalid prompt/messages"}
            return

        url = f"{_ollama_base_url()}{path}"

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                resp = await client.post(url, json=body)
                if resp.status_code != 200:
                    yield {"error": f"HTTP {resp.status_code}: {resp.text}"}
                    return
                yield resp.json()
        except httpx.RequestError as e:
            yield {"error": str(e)}

    def _image_classification_body(self, encoded_image_b64: str, model: str) -> dict:
        return {
            "model": model,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Analyze this image and return only a JSON array of short keyword strings. "
                        "Capture content, atmosphere, vibe, and location, objects, people, time periodand any other relevant information. "
                        "Use 8 to 20 concise keywords. Do not include any text outside the JSON array."
                    ),
                    "images": [encoded_image_b64],
                }
            ],
            "options": {"temperature": 0.2},
        }

    def _image_question_body(self, encoded_image_b64: str, prompt: str, model: str) -> dict:
        return {
            "model": model,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        prompt
                    ),
                    "images": [encoded_image_b64],
                }
            ],
            "options": {"temperature": 0.2},
        }
