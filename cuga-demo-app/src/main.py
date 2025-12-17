#!/usr/bin/env python3
"""
CUGA Demo Application - Main Entry Point

This module demonstrates the core usage of CUGA agent with various configurations
and execution modes.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import output logger
from src.utils.output_logger import create_logger

# Load environment variables
load_dotenv()

console = Console()

# Create output logger for main script
logger = create_logger("main")


class CUGADemo:
    """Main CUGA demonstration class."""
    
    def __init__(self, mode: str = "balanced", task_mode: str = "api"):
        """
        Initialize CUGA demo.
        
        Args:
            mode: Reasoning mode (fast, balanced, accurate)
            task_mode: Task execution mode (api, web, hybrid)
        """
        self.mode = mode
        self.task_mode = task_mode
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from TOML files."""
        import toml
        
        config_path = project_root / "config" / "settings.toml"
        mode_config_path = project_root / "config" / "modes" / f"{self.mode}.toml"
        
        config = {}
        if config_path.exists():
            config.update(toml.load(config_path))
        if mode_config_path.exists():
            mode_config = toml.load(mode_config_path)
            # Merge mode-specific config
            for key, value in mode_config.items():
                if key in config and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
                    
        return config
    
    def display_config(self):
        """Display current configuration."""
        table = Table(title="CUGA Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Reasoning Mode", self.mode)
        table.add_row("Task Mode", self.task_mode)
        
        # Detect provider
        provider = self._detect_provider()
        table.add_row("LLM Provider", provider)
        table.add_row("Model", os.getenv("MODEL_NAME", "Default"))
        
        # Show base URL if using Ollama or custom endpoint
        base_url = os.getenv("OPENAI_BASE_URL", "")
        if base_url and "localhost" in base_url:
            table.add_row("Base URL", base_url)
        
        console.print(table)
    
    def _detect_provider(self) -> str:
        """Detect which LLM provider is being used."""
        base_url = os.getenv("OPENAI_BASE_URL", "")
        
        if "localhost:11434" in base_url or os.getenv("OPENAI_API_KEY") == "ollama":
            return "Ollama (Local)"
        elif os.getenv("WATSONX_API_KEY"):
            return "IBM watsonx"
        elif os.getenv("AZURE_OPENAI_API_KEY"):
            return "Azure OpenAI"
        elif os.getenv("OPENROUTER_API_KEY"):
            return "OpenRouter"
        elif os.getenv("OPENAI_API_KEY"):
            return "OpenAI"
        else:
            return "Not configured"
    
    def execute_task(self, task: str) -> dict:
        """
        Execute a task using CUGA agent.
        
        Args:
            task: Task description
            
        Returns:
            Execution result
        """
        console.print(Panel(f"[bold blue]Executing Task:[/bold blue] {task}"))
        
        # This is a simplified demonstration
        # In a real implementation, you would:
        # 1. Initialize the CUGA agent with proper configuration
        # 2. Load tools from the registry
        # 3. Execute the task through the agent
        # 4. Return structured results
        
        result = {
            "task": task,
            "mode": self.mode,
            "task_mode": self.task_mode,
            "status": "simulated",
            "message": "This is a demonstration. Integrate actual CUGA agent for real execution."
        }
        
        console.print("[green]✓[/green] Task execution simulated")
        return result


@click.group()
def cli():
    """CUGA Demo Application - Command Line Interface"""
    pass


@cli.command()
@click.option("--mode", default="balanced",
              type=click.Choice(["fast", "balanced", "accurate"]),
              help="Reasoning mode")
@click.option("--task-mode", default="api",
              type=click.Choice(["api", "web", "hybrid"]),
              help="Task execution mode")
@click.option("--task", prompt="Enter task", help="Task to execute")
def run(mode: str, task_mode: str, task: str):
    """Run a single task with CUGA."""
    logger.log_section("Task Execution", f"Mode: {mode}, Task Mode: {task_mode}")
    logger.log_text(f"**Task:** {task}")
    
    demo = CUGADemo(mode=mode, task_mode=task_mode)
    demo.display_config()
    result = demo.execute_task(task)
    
    console.print("\n[bold]Result:[/bold]")
    console.print(result)
    
    # Log result
    logger.log_result(result)
    logger.finalize()
    console.print(f"\n[dim]Output saved to: {logger.get_filepath()}[/dim]")


@cli.command()
@click.option("--mode", default="balanced",
              type=click.Choice(["fast", "balanced", "accurate"]),
              help="Reasoning mode")
def interactive(mode: str):
    """Start interactive CUGA session."""
    console.print(Panel.fit(
        "[bold cyan]CUGA Interactive Mode[/bold cyan]\n"
        "Type 'exit' or 'quit' to end session\n"
        "Type 'config' to view configuration\n"
        "Type 'help' for available commands",
        border_style="cyan"
    ))
    
    demo = CUGADemo(mode=mode)
    
    while True:
        try:
            task = console.input("\n[bold cyan]CUGA>[/bold cyan] ")
            
            if task.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif task.lower() == "config":
                demo.display_config()
            elif task.lower() == "help":
                console.print("""
[bold]Available Commands:[/bold]
  - Type any task to execute it
  - 'config' - View current configuration
  - 'help' - Show this help message
  - 'exit' or 'quit' - End session
                """)
            elif task.strip():
                demo.execute_task(task)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")


@cli.command()
def examples():
    """Show example tasks and usage."""
    console.print(Panel.fit(
        "[bold cyan]CUGA Example Tasks[/bold cyan]",
        border_style="cyan"
    ))
    
    examples_list = [
        ("CRM Operations", "get top 5 accounts by revenue from digital sales"),
        ("Data Analysis", "analyze customer sentiment from recent feedback"),
        ("Web Automation", "go to dashboard and extract latest sales figures"),
        ("Hybrid Task", "get top account by revenue from API, then add it to current page"),
        ("File Operations", "read cities.txt and company.txt, find common cities"),
    ]
    
    table = Table(title="Example Tasks")
    table.add_column("Category", style="cyan")
    table.add_column("Task", style="green")
    
    for category, task in examples_list:
        table.add_row(category, task)
    
    console.print(table)
    
    console.print("\n[bold]To run an example:[/bold]")
    console.print("  python src/main.py run --task 'your task here'")


@cli.command()
def check_setup():
    """Check if environment is properly configured."""
    console.print(Panel.fit(
        "[bold cyan]CUGA Setup Check[/bold cyan]",
        border_style="cyan"
    ))
    
    checks = []
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("WATSONX_API_KEY") or \
              os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    
    # For Ollama, API key can be "ollama" (dummy value)
    is_ollama = os.getenv("OPENAI_API_KEY") == "ollama" or \
                "localhost:11434" in os.getenv("OPENAI_BASE_URL", "")
    
    ollama_running = False
    if is_ollama:
        checks.append(("LLM Provider", "Ollama (Local)", "cyan"))
        # Check if Ollama is accessible
        import httpx
        try:
            response = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
            ollama_running = response.status_code == 200
            checks.append(("Ollama Service", "✓ Running" if ollama_running else "✗ Not running",
                          "green" if ollama_running else "red"))
        except:
            checks.append(("Ollama Service", "✗ Not accessible", "red"))
    else:
        checks.append(("API Key", "✓" if api_key else "✗", "green" if api_key else "red"))
    
    # Check config files
    config_exists = (project_root / "config" / "settings.toml").exists()
    checks.append(("Config File", "✓" if config_exists else "✗", 
                   "green" if config_exists else "red"))
    
    # Check .env file
    env_exists = (project_root / ".env").exists()
    checks.append((".env File", "✓" if env_exists else "✗",
                   "green" if env_exists else "yellow"))
    
    table = Table(title="Setup Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    
    for component, status, color in checks:
        table.add_row(component, f"[{color}]{status}[/{color}]")
    
    console.print(table)
    
    if is_ollama:
        if not ollama_running:
            console.print("\n[yellow]⚠ Warning:[/yellow] Ollama service is not running.")
            console.print("[yellow]💡 Tip:[/yellow] Start Ollama with: ollama serve")
            console.print("[yellow]💡 Tip:[/yellow] Or install from: https://ollama.ai")
        else:
            console.print("\n[green]✓ Ollama is configured and running![/green]")
            console.print(f"[cyan]Model:[/cyan] {os.getenv('MODEL_NAME', 'llama3.2')}")
    elif not api_key:
        console.print("\n[yellow]⚠ Warning:[/yellow] No API key found. "
                     "Please set up your .env file.")
    
    if not env_exists:
        console.print("\n[yellow]💡 Tip:[/yellow] Copy .env.example to .env "
                     "and configure your LLM provider.")
        console.print("[yellow]💡 Recommended:[/yellow] Use Ollama for free local LLM!")


if __name__ == "__main__":
    cli()

# Made with Bob
