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
        """
        Build a prompt for creating a new shift handoff brief.

        Requirements:
        - Reject None, empty, or whitespace-only notes with ValueError.
        - Include the original shift notes in the prompt.
        - Include every required section label from REQUIRED_SECTIONS.
        - Tell the model not to invent unsupported details.
        - Tell the model to use "Unknown" when details are not provided.
        - Keep this domain-specific prompt logic in this builder class,
          not in the reusable AI client.
        """
        # TODO: Validate notes.
        # TODO: Build and return a prompt for a new handoff brief.
        pass

    def build_revision_prompt(self, feedback):
        """
        Build a prompt for revising the previous handoff brief.

        Requirements:
        - Reject None, empty, or whitespace-only feedback with ValueError.
        - Reference the previous brief or earlier conversation.
        - Include the manager's revision feedback.
        - Include every required section label from REQUIRED_SECTIONS.
        - Tell the model not to invent unsupported details.
        """
        # TODO: Validate feedback.
        # TODO: Build and return a revision prompt.
        pass

    def is_usable_brief(self, response_text):
        """
        Check whether the AI response includes the required handoff structure.

        Requirements:
        - Return False for None, empty, or whitespace-only responses.
        - Return True only when the response contains every required section label.
        - Return False if one or more required sections are missing.
        """
        # TODO: Check whether response_text contains all required sections.
        pass

    def format_brief(self, response_text):
        """
        Format a created handoff brief for display.

        Requirements:
        - Return a string.
        - Add a clear user-facing heading before the response text.
        - Preserve the AI response content.
        """
        # TODO: Return a formatted created-brief string.
        pass

    def create_brief(self, ai_client, notes):
        """
        Create a new handoff brief.

        Requirements:
        - Build a prompt from the shift notes.
        - Send the prompt through ai_client.send().
        - Verify that the AI response includes the required sections.
        - Raise RuntimeError if the AI response is not usable.
        - Return a formatted user-facing brief.
        """
        # TODO: Build the prompt.
        # TODO: Send the prompt through the AI client.
        # TODO: Verify the response structure.
        # TODO: Return the formatted brief.
        pass

    def revise_brief(self, ai_client, feedback):
        """
        Revise the previous handoff brief.

        Requirements:
        - Build a revision prompt from the feedback.
        - Send the prompt through ai_client.send().
        - Verify that the AI response includes the required sections.
        - Raise RuntimeError if the AI response is not usable.
        - Return a formatted user-facing revised brief.
        """
        # TODO: Build the revision prompt.
        # TODO: Send the prompt through the AI client.
        # TODO: Verify the response structure.
        # TODO: Return the formatted revised brief.
        pass