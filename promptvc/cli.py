import typer
from promptvc.repo import PromptRepo
import os
import json

from .llm import call_openai, call_anthropic

LLM_CALLERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
}

app = typer.Typer(help="Git-like version control for LLM prompts.")

@app.command()
def init(path="."):
    config_path = os.path.join(path, "promptvc.yaml")
    if not os.path.exists(config_path):
        typer.echo("Config file 'promptvc.yaml' not found. Creating a template...")
        template_config = """\
# This will store the config for all your LLM providers..
llm_providers:
  openai:
    api_key: "sk-..."
    default_model: "gpt-4-turbo"
  anthropic:
    api_key: "api-key-..."
    default_model: "claude-3-opus-20240229"
"""
        with open(config_path, "w") as f:
            f.write(template_config)
        typer.echo(f"Created promptvc.yaml")
    else:
        typer.echo("Config file 'promptvc.yaml' already exists.")

    gitignore_path = os.path.join(path, ".gitignore")
    config_filename = "promptvc.yaml"
    try:
        with open(gitignore_path, "a+") as f:
            f.seek(0)
            lines = f.readlines()
            found = False
            for line in lines:
                if config_filename in line:
                    found = True
                    break
            if not found:
                f.write(f"\n# promptvc configuration file\n{config_filename}\n")
                typer.echo(f"Added '{config_filename}' to .gitignore.")
    except IOError as e:
        typer.echo(f"Could not write to .gitignore: {e}", err=True)

    repo = PromptRepo(path)
    typer.echo(f"Initialized prompt repo at {repo.repo_path}")

@app.command()
def add(name, text):
    repo = PromptRepo()
    repo.add(name, text)
    typer.echo(f"Added/updated prompt '{name}' (staged).")

@app.command()
def commit(name, msg):
    repo = PromptRepo()
    repo.commit(name, msg)
    typer.echo(f"Committed prompt '{name}' with message: {msg}")

@app.command()
def history(name):
    repo = PromptRepo()
    versions = repo.history(name)
    for v in versions:
        typer.echo(f"Version {v.id}: {v.commit_msg} ({v.timestamp})")

@app.command()
def checkout(name, version):
    repo = PromptRepo()
    text = repo.checkout(name, version)
    if text:
        typer.echo(text)
    else:
        typer.echo("Version not found")

@app.command()
def diff(name, v1, v2):
    repo = PromptRepo()
    result = repo.diff(name, v1, v2)
    typer.echo("Text Diff:\n" + result["text_diff"])
    typer.echo(f"\nSemantic Similarity: {result['semantic_similarity']:.2f}")

@app.command(name="list")
def list_prompts():
    repo = PromptRepo()
    files = os.listdir(repo.prompts_dir)
    for f in files:
        if f.endswith('.yaml') and '_baseline' not in f:
            typer.echo(f.replace('.yaml', ''))

@app.command()
def set_baseline(name, version, samples_file, llm="openai"):
    repo = PromptRepo()
    
    if llm not in LLM_CALLERS:
        available_llms = []
        for key in LLM_CALLERS.keys():
            available_llms.append(key)
        typer.echo(f"Error: Invalid LLM specified. Choose from {available_llms}", err=True)
        raise typer.Exit(code=1)

    with open(samples_file, 'r') as f:
        samples = json.load(f)
    
    typer.echo(f"Setting version {version} of '{name}' as baseline using {llm}... (This may take a moment)")
    repo.set_baseline(name, version, samples, llm_func=LLM_CALLERS[llm])
    typer.echo(f"Baseline set")

@app.command()
def compare_baseline(name, version, samples_file, llm="openai"):
    repo = PromptRepo()

    if llm not in LLM_CALLERS:
        available_llms = []
        for key in LLM_CALLERS.keys():
            available_llms.append(key)
        typer.echo(f"Error: Invalid LLM specified. Choose from {available_llms}", err=True)
        raise typer.Exit(code=1)
        
    with open(samples_file, 'r') as f:
        samples = json.load(f)

    typer.echo(f"Comparing version {version} of '{name}' to baseline using {llm}... (This may take a moment)")
    try:
        results = repo.compare_to_baseline(name, version, samples, llm_func=LLM_CALLERS[llm])
        
        typer.echo("\n--- Comparison Report ---")
        for comp in results['comparisons']:
            typer.echo("\n" + "="*20)
            typer.echo(f"Input: {comp['input']}")
            typer.echo(f" - Baseline (v{results['baseline_version']}) Output: {comp['baseline_output']}")
            typer.echo(f" - New (v{results['new_version']}) Output: {comp['new_output']}")
            typer.echo(f" - Similarity: {comp['similarity']:.2f}")
    except (ValueError, FileNotFoundError) as e:
        typer.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    app()