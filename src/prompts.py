"""Summary prompt templates, keyed by the detail level exposed in the UI."""

CONCISE = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."

STANDARD = (
    "Summarize the main content of the uploaded PDF file in a clear, well-organized "
    "paragraph of about 150-250 words, covering what it's about and its key points."
)

DETAILED = """Provide a detailed, engaging summary of the document structured as follows:

1. Overview: A 2-3 sentence introduction to what this document is and its core subject.
2. Setup: How the document begins — the initial situation, context, or premise.
3. Development: What happens next — the key events, arguments, or content that unfolds.
4. Outcome: How it concludes — the result, resolution, or final takeaway.

Write in full paragraphs under each heading, with enough detail that someone who hasn't
read the document understands not just what it's about, but how it unfolds."""

PROMPTS = {
    "Concise": CONCISE,
    "Standard": STANDARD,
    "Detailed": DETAILED,
}

DEFAULT_LEVEL = "Detailed"
