class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        """Build a prompt for creating a new shift handoff brief."""
        if notes is None or not isinstance(notes, str) or not notes.strip():
            raise ValueError("Shift notes cannot be empty")

        cleaned_notes = notes.strip()
        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "Create a concise shift handoff brief from the following notes. "
            "Use the required sections below and do not invent unsupported details. "
            "If something is not provided, write 'Unknown'.\n\n"
            f"Shift Notes:\n{cleaned_notes}\n\n"
            f"Required sections:\n{sections}\n"
        )

    def build_revision_prompt(self, feedback):
        """Build a prompt for revising the previous handoff brief."""
        if feedback is None or not isinstance(feedback, str) or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty")

        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "Revise the previous handoff brief using the manager feedback below. "
            "Reference the earlier conversation context and keep the response in the same structure. "
            "Do not invent unsupported details or add facts that are not present in the notes. "
            "If any detail is missing, use 'Unknown'.\n\n"
            f"Manager Feedback:\n{feedback.strip()}\n\n"
            f"Required sections:\n{sections}\n"
        )

    def is_usable_brief(self, response_text):
        """Check whether the AI response contains the required handoff sections."""
        if response_text is None or not isinstance(response_text, str) or not response_text.strip():
            return False

        text = response_text.strip()
        return all(section in text for section in self.REQUIRED_SECTIONS)

    def format_brief(self, response_text):
        """Format a created handoff brief for display."""
        return f"\nShift Handoff Brief\n{response_text.strip()}"

    def create_brief(self, ai_client, notes):
        """Create a new handoff brief using the AI client."""
        prompt = self.build_brief_prompt(notes)
        response_text = ai_client.send(prompt)

        if not self.is_usable_brief(response_text):
            raise RuntimeError("AI response did not include required sections")

        return self.format_brief(response_text)

    def revise_brief(self, ai_client, feedback):
        """Revise a previous handoff brief using the AI client."""
        prompt = self.build_revision_prompt(feedback)
        response_text = ai_client.send(prompt)

        if not self.is_usable_brief(response_text):
            raise RuntimeError("AI response did not include required sections")

        return f"\nRevised Shift Handoff Brief\n{response_text.strip()}"