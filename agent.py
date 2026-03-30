import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

REVIEW_SYSTEM_PROMPT = """
You are an expert code reviewer. When given a code snippet, analyze it and
return a structured review in the following JSON format only — no markdown,
no explanation outside the JSON:

{
  "summary": "One sentence overview of the code's purpose and quality",
  "issues": [
    {
      "line_hint": "approximate line or block reference (e.g., 'line 5', 'function foo')",
      "severity": "critical | warning | info",
      "description": "What the issue is",
      "suggestion": "How to fix or improve it"
    }
  ],
  "overall_score": "1-10 integer rating of code quality",
  "positive_notes": ["list of things done well"]
}

Rules:
- Always return valid JSON only.
- severity must be exactly one of: critical, warning, info
- If no issues found, return an empty issues array.
- Be specific, practical, and helpful — like a senior engineer doing a real PR review.
"""

# --- Tool: Save user code to state ---
def save_code_to_state(
    tool_context: ToolContext, code: str, language: str = "auto-detect"
) -> dict[str, str]:
    """Saves the user's submitted code and language to the session state."""
    tool_context.state["CODE"] = code
    tool_context.state["LANGUAGE"] = language
    logging.info(f"[State updated] Code saved. Language: {language}")
    return {"status": "success"}

# --- Agent 1: Code Analyzer ---
code_analyzer = Agent(
    name="code_analyzer",
    model=model_name,
    description="Analyzes the submitted code and produces a structured JSON review.",
    instruction="""
    You are an expert code reviewer.
    Analyze the following code submitted by the user.

    Language: {LANGUAGE}
    Code:
    {CODE}

    """ + REVIEW_SYSTEM_PROMPT,
    output_key="review_data"
)

# --- Agent 2: Response Formatter ---
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Presents the code review in a clear, friendly, and readable format.",
    instruction="""
    You are a helpful assistant presenting a code review result to a developer.
    Take the REVIEW_DATA below and present it in a clean, human-readable format.

    - Start with the summary.
    - List each issue with its severity, location, description, and suggestion.
    - Show the overall score.
    - End with the positive notes to encourage the developer.
    - Be constructive, clear, and friendly.

    REVIEW_DATA:
    {review_data}
    """
)

# --- Sequential Workflow ---
review_workflow = SequentialAgent(
    name="review_workflow",
    description="Runs the full code review pipeline: analyze then format.",
    sub_agents=[
        code_analyzer,      # Step 1: Analyze the code
        response_formatter, # Step 2: Format the output
    ]
)

# --- Root Agent (Entry Point) ---
root_agent = Agent(
    name="code_review_greeter",
    model=model_name,
    description="The main entry point for the Code Review Agent.",
    instruction="""
    You are a helpful code review assistant.
    - Greet the user and ask them to paste the code they want reviewed,
      and optionally specify the programming language.
    - When the user provides code, use the 'save_code_to_state' tool to save it.
    - After saving, transfer control to the 'review_workflow' agent.
    """,
    tools=[save_code_to_state],
    sub_agents=[review_workflow]
)