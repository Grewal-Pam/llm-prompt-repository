from repository import create_prompt, get_prompts
from models import PromptCreate

def seed_wolfram_prompts():
    existing = get_prompts()
    if existing:
        return

    seeds = [
        PromptCreate(
            title="ClickBaitTitle",
            prompt_text="Rewrite the given text as a clickbait-style headline.",
            purpose="Text rewriting",
            tags=["headline", "rewriting"],
            source="https://resources.wolframcloud.com/PromptRepository/resources/ClickBaitTitle/"
        ),
        PromptCreate(
            title="CodeDocAnnotator",
            prompt_text="Generate clear documentation annotations for the given source code.",
            purpose="Code documentation",
            tags=["code", "documentation"],
            source="https://resources.wolframcloud.com/PromptRepository/resources/CodeDocAnnotator/"
        ),
        PromptCreate(
            title="MermaidDiagram",
            prompt_text="Generate a Mermaid.js diagram from a textual description.",
            purpose="Visualization",
            tags=["diagram", "visualization"],
            source="https://resources.wolframcloud.com/PromptRepository/resources/MermaidDiagram/"
        )
    ]

    for prompt in seeds:
        create_prompt(prompt)
