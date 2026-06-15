from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """Initialize the CLI application with an AI client and builder."""
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """Print a welcome message and command guidance."""
        print("Shift Handoff Brief CLI")
        print(self.command_help())

    def command_help(self):
        """Return command guidance as a string."""
        return (
            "Available commands:\n"
            "  brief <shift notes>   Create a handoff brief\n"
            "  revise <feedback>     Revise the current brief\n"
            "  history               Show the number of stored messages\n"
            "  reset                 Clear conversation history\n"
            "  help                  Show this help message\n"
            "  exit or quit          Exit the CLI"
        )

    def handle_command(self, raw_input):
        """Route a user command and return the response text."""
        if raw_input is None or not isinstance(raw_input, str) or not raw_input.strip():
            return "Input error: please enter a command."

        text = raw_input.strip()
        lowered = text.lower()

        if lowered in ("exit", "quit"):
            self.running = False
            return "Goodbye!"

        if lowered == "help":
            return self.command_help()

        if lowered == "history":
            count = self.ai_client.message_count()
            return f"Conversation messages: {count}"

        if lowered == "reset":
            self.ai_client.reset()
            return "Conversation history reset."

        if lowered.startswith("brief"):
            payload = text[5:].strip()
            if not payload:
                return "Input error: 'brief' requires shift notes."
            try:
                return self.brief_builder.create_brief(self.ai_client, payload)
            except ValueError as exc:
                return f"Input error: {exc}"
            except RuntimeError as exc:
                return f"Service error: {exc}"

        if lowered.startswith("revise"):
            payload = text[6:].strip()
            if not payload:
                return "Input error: 'revise' requires revision feedback."
            try:
                return self.brief_builder.revise_brief(self.ai_client, payload)
            except ValueError as exc:
                return f"Input error: {exc}"
            except RuntimeError as exc:
                return f"Service error: {exc}"

        return (
            "Input error: unknown command. Type 'help' to see the available commands."
        )

    def run(self):
        """Run the CLI input loop and print responses."""
        self.display_welcome()

        while self.running:
            try:
                user_input = input(" > ")
            except EOFError:
                print("Goodbye!")
                self.running = False
                break

            response = self.handle_command(user_input)
            if response:
                print(response)


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()