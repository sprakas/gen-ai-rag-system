from langchain_community.llms import Ollama

class LLMService:
    def __init__(self):
        self.llm = Ollama(model="llama3.2:1b")

    def generate(self, prompt):
        return self.llm.invoke(prompt)