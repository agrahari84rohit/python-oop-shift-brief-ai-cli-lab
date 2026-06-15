import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """Initialize the client with a model name and empty history."""
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        """Send a prompt to the AI service and return the assistant response text."""
        if prompt is None or not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        cleaned_prompt = prompt.strip()
        user_message = {"role": "user", "content": cleaned_prompt}
        self.history.append(user_message)

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)

            content = None
            if isinstance(response, dict):
                message = response.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
            else:
                message = getattr(response, "message", None)
                if isinstance(message, dict):
                    content = message.get("content")
                else:
                    content = getattr(message, "content", None)

            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("AI service request failed: no usable assistant response")

            assistant_message = {"role": "assistant", "content": content.strip()}
            self.history.append(assistant_message)
            return assistant_message["content"]
        except Exception as exc:
            if self.history and self.history[-1] == user_message:
                self.history.pop()
            raise RuntimeError(f"AI service request failed: {exc}") from exc

    def reset(self):
        """Clear the conversation history."""
        self.history = []

    def message_count(self):
        """Return the number of messages currently stored in conversation history."""
        return len(self.history)

    def get_transcript(self):
        """Return a safe copy of the conversation history."""
        return [dict(message) for message in self.history]