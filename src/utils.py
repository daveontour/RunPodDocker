class JobInput:
    def __init__(self, job):
        self.prompt = job.get("prompt")
        self.list_models = bool(job.get("list_models", False))
        self.imageClassifyRequestTest = job.get("imageClassifyRequestTest", False)
        self.embeddingRequest = job.get("embeddingRequest")
        self.imageClassifyRequest = job.get("imageClassifyRequest")
        self.imageQuestionRequest = job.get("imageQuestionRequest")
        self.question = job.get("question")