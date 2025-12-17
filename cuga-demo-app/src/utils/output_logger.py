#!/usr/bin/env python3
"""
Output Logger Utility

Creates timestamped markdown files in the ./output folder for script execution logs.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
import json


class OutputLogger:
    """Logger that creates timestamped markdown files for script outputs."""
    
    def __init__(self, script_name: str, output_dir: str = "./output"):
        """
        Initialize the output logger.
        
        Args:
            script_name: Name of the script (without .py extension)
            output_dir: Directory to save output files (default: ./output)
        """
        self.script_name = script_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{script_name}_{timestamp}.md"
        self.filepath = self.output_dir / self.filename
        
        # Initialize the markdown file
        self._initialize_file()
    
    def _initialize_file(self):
        """Initialize the markdown file with header."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {self.script_name} - Execution Log\n\n")
            f.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
    
    def log_section(self, title: str, content: str = ""):
        """
        Log a section to the markdown file.
        
        Args:
            title: Section title
            content: Section content
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"## {title}\n\n")
            if content:
                f.write(f"{content}\n\n")
    
    def log_code(self, code: str, language: str = "python"):
        """
        Log code block to the markdown file.
        
        Args:
            code: Code to log
            language: Programming language for syntax highlighting
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"```{language}\n{code}\n```\n\n")
    
    def log_data(self, data: Any, title: Optional[str] = None):
        """
        Log data (dict, list, etc.) as formatted JSON.
        
        Args:
            data: Data to log
            title: Optional title for the data section
        """
        if title:
            self.log_section(title)
        
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write("```json\n")
            f.write(json.dumps(data, indent=2, default=str))
            f.write("\n```\n\n")
    
    def log_table(self, headers: list, rows: list):
        """
        Log a markdown table.
        
        Args:
            headers: List of column headers
            rows: List of rows (each row is a list of values)
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            # Write headers
            f.write("| " + " | ".join(str(h) for h in headers) + " |\n")
            f.write("| " + " | ".join("---" for _ in headers) + " |\n")
            
            # Write rows
            for row in rows:
                f.write("| " + " | ".join(str(cell) for cell in row) + " |\n")
            f.write("\n")
    
    def log_text(self, text: str):
        """
        Log plain text to the markdown file.
        
        Args:
            text: Text to log
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"{text}\n\n")
    
    def log_list(self, items: list, ordered: bool = False):
        """
        Log a list to the markdown file.
        
        Args:
            items: List of items to log
            ordered: If True, create numbered list; otherwise bullet list
        """
        with open(self.filepath, 'a', encoding='utf-8') as f:
            for i, item in enumerate(items, 1):
                if ordered:
                    f.write(f"{i}. {item}\n")
                else:
                    f.write(f"- {item}\n")
            f.write("\n")
    
    def log_result(self, result: dict):
        """
        Log execution result with status.
        
        Args:
            result: Result dictionary with status and other info
        """
        status = result.get('status', 'unknown')
        status_emoji = "✅" if status == "success" else "❌" if status == "error" else "ℹ️"
        
        self.log_section("Execution Result")
        self.log_text(f"{status_emoji} **Status:** {status}")
        
        if 'message' in result:
            self.log_text(f"**Message:** {result['message']}")
        
        if 'data' in result:
            self.log_data(result['data'], "Result Data")
        
        if 'execution_time' in result:
            self.log_text(f"**Execution Time:** {result['execution_time']}")
    
    def finalize(self):
        """Add footer to the markdown file."""
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write("\n---\n\n")
            f.write(f"*Log generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    def get_filepath(self) -> Path:
        """Get the path to the output file."""
        return self.filepath


def create_logger(script_name: str) -> OutputLogger:
    """
    Convenience function to create an output logger.
    
    Args:
        script_name: Name of the script
        
    Returns:
        OutputLogger instance
    """
    return OutputLogger(script_name)

# Made with Bob
