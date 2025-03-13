from google import genai
from dotenv import dotenv_values
from typing import Optional


class GeminiSummarizer:
    def __init__(self, model: str = "gemini-2.0-flash"):
        config = dotenv_values(".env")
        self.client = genai.Client(api_key=config["GEMINI_API_KEY"])
        self.model = model

    def _generate_summary_prompt(self, text: str) -> str:
        return f"""Please provide a concise summary of the following text. Focus on the key points and main ideas:

{text}

Summary:"""

    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        prompt = self._generate_summary_prompt(text)
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        summary = response.text.strip()

        if max_length and len(summary) > max_length:
            summary = summary[:max_length].rsplit(".", 1)[0] + "."

        return summary


if __name__ == "__main__":
    summarizer = GeminiSummarizer()
    sample_text = "Artificial Intelligence (AI) is revolutionizing various industries, from healthcare to finance. It enables machines to learn from experience, adjust to new inputs, and perform human-like tasks. Machine learning, a subset of AI, focuses on the development of computer programs that can access data and use it to learn for themselves."
    print(summarizer.summarize(sample_text))
