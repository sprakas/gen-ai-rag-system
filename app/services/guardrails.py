import re

class Guardrails:

    @staticmethod
    def detect_prompt_injection(query: str) -> bool:
        patterns = [
            "ignore previous instructions",
            "system prompt",
            "act as",
            "bypass"
        ]
        return any(p in query.lower() for p in patterns)

    @staticmethod
    def sanitize_input(query: str) -> str:
        # remove suspicious patterns
        return re.sub(r"(ignore.*|system prompt.*|act as.*|bypass.*)", "", query, flags=re.IGNORECASE)

    @staticmethod
    def validate_output(answer: str) -> str:
        if "I don't know" in answer:
            return "Sorry, I couldn't find relevant information."

        return answer