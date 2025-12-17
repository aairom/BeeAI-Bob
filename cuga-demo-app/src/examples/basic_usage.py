#!/usr/bin/env python3
"""
CUGA Basic Usage Examples

This module demonstrates basic CUGA agent usage patterns including:
- Simple task execution
- Configuration management
- Error handling
- Result processing
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import output logger
from src.utils.output_logger import create_logger


class BasicCUGAExample:
    """Basic CUGA usage examples."""
    
    def __init__(self):
        """Initialize basic example."""
        self.results = []
        
    def example_1_simple_task(self) -> Dict[str, Any]:
        """
        Example 1: Execute a simple task
        
        Demonstrates:
        - Basic task execution
        - Result retrieval
        """
        print("\n" + "="*60)
        print("Example 1: Simple Task Execution")
        print("="*60)
        
        task = "List all accounts in the CRM system"
        
        print(f"\nTask: {task}")
        print("\nIn a real implementation, this would:")
        print("1. Initialize CUGA agent with configuration")
        print("2. Load necessary tools (CRM API)")
        print("3. Execute the task through the agent")
        print("4. Return structured results")
        
        # Simulated result
        result = {
            "task": task,
            "status": "success",
            "data": [
                {"id": 1, "name": "Acme Corp", "revenue": 1000000},
                {"id": 2, "name": "TechStart Inc", "revenue": 750000},
                {"id": 3, "name": "Global Solutions", "revenue": 2000000}
            ],
            "execution_time": "2.3s",
            "mode": "balanced"
        }
        
        print(f"\nResult: {result['status']}")
        print(f"Accounts found: {len(result['data'])}")
        
        self.results.append(result)
        return result
    
    def example_2_with_parameters(self) -> Dict[str, Any]:
        """
        Example 2: Task with parameters
        
        Demonstrates:
        - Parameterized task execution
        - Filtering and sorting
        """
        print("\n" + "="*60)
        print("Example 2: Task with Parameters")
        print("="*60)
        
        task = "Get top 3 accounts by revenue"
        
        print(f"\nTask: {task}")
        print("\nThis demonstrates:")
        print("- Parameter extraction from natural language")
        print("- API call with filters and sorting")
        print("- Result limiting")
        
        # Simulated result
        result = {
            "task": task,
            "status": "success",
            "data": [
                {"id": 3, "name": "Global Solutions", "revenue": 2000000},
                {"id": 1, "name": "Acme Corp", "revenue": 1000000},
                {"id": 2, "name": "TechStart Inc", "revenue": 750000}
            ],
            "parameters": {
                "limit": 3,
                "sort_by": "revenue",
                "order": "desc"
            },
            "execution_time": "1.8s",
            "mode": "balanced"
        }
        
        print(f"\nResult: {result['status']}")
        print(f"Top accounts: {len(result['data'])}")
        for i, account in enumerate(result['data'], 1):
            print(f"  {i}. {account['name']}: ${account['revenue']:,}")
        
        self.results.append(result)
        return result
    
    def example_3_error_handling(self) -> Dict[str, Any]:
        """
        Example 3: Error handling
        
        Demonstrates:
        - Graceful error handling
        - Retry mechanisms
        - Error reporting
        """
        print("\n" + "="*60)
        print("Example 3: Error Handling")
        print("="*60)
        
        task = "Get account with invalid ID: -999"
        
        print(f"\nTask: {task}")
        print("\nThis demonstrates:")
        print("- Input validation")
        print("- Error detection and handling")
        print("- Informative error messages")
        
        # Simulated error result
        result = {
            "task": task,
            "status": "error",
            "error": {
                "type": "ValidationError",
                "message": "Invalid account ID: -999",
                "details": "Account ID must be a positive integer"
            },
            "execution_time": "0.5s",
            "mode": "balanced"
        }
        
        print(f"\nResult: {result['status']}")
        print(f"Error: {result['error']['message']}")
        print(f"Details: {result['error']['details']}")
        
        self.results.append(result)
        return result
    
    def example_4_multi_step_task(self) -> Dict[str, Any]:
        """
        Example 4: Multi-step task execution
        
        Demonstrates:
        - Task decomposition
        - Sequential execution
        - Intermediate results
        """
        print("\n" + "="*60)
        print("Example 4: Multi-Step Task")
        print("="*60)
        
        task = "Find the highest revenue account and get its contact details"
        
        print(f"\nTask: {task}")
        print("\nThis demonstrates:")
        print("- Automatic task decomposition")
        print("- Sequential step execution")
        print("- Data passing between steps")
        
        # Simulated result with steps
        result = {
            "task": task,
            "status": "success",
            "steps": [
                {
                    "step": 1,
                    "action": "Get all accounts sorted by revenue",
                    "status": "completed",
                    "duration": "1.2s"
                },
                {
                    "step": 2,
                    "action": "Select top account",
                    "status": "completed",
                    "duration": "0.1s"
                },
                {
                    "step": 3,
                    "action": "Fetch contact details for account ID 3",
                    "status": "completed",
                    "duration": "0.8s"
                }
            ],
            "data": {
                "account": {
                    "id": 3,
                    "name": "Global Solutions",
                    "revenue": 2000000
                },
                "contacts": [
                    {"name": "John Doe", "email": "john@global.com", "role": "CEO"},
                    {"name": "Jane Smith", "email": "jane@global.com", "role": "CFO"}
                ]
            },
            "execution_time": "2.1s",
            "mode": "balanced"
        }
        
        print(f"\nResult: {result['status']}")
        print(f"Steps executed: {len(result['steps'])}")
        print(f"\nAccount: {result['data']['account']['name']}")
        print(f"Revenue: ${result['data']['account']['revenue']:,}")
        print(f"Contacts: {len(result['data']['contacts'])}")
        
        self.results.append(result)
        return result
    
    def example_5_mode_comparison(self):
        """
        Example 5: Compare different reasoning modes
        
        Demonstrates:
        - Fast mode (speed optimized)
        - Balanced mode (default)
        - Accurate mode (precision optimized)
        """
        print("\n" + "="*60)
        print("Example 5: Reasoning Mode Comparison")
        print("="*60)
        
        task = "Analyze sales trends for Q4 2024"
        
        modes = ["fast", "balanced", "accurate"]
        
        print(f"\nTask: {task}")
        print("\nComparing execution across different modes:\n")
        
        for mode in modes:
            # Simulated results for different modes
            if mode == "fast":
                result = {
                    "mode": mode,
                    "execution_time": "1.2s",
                    "steps": 3,
                    "accuracy": "good",
                    "description": "Quick analysis with basic insights"
                }
            elif mode == "balanced":
                result = {
                    "mode": mode,
                    "execution_time": "2.5s",
                    "steps": 5,
                    "accuracy": "very good",
                    "description": "Thorough analysis with detailed insights"
                }
            else:  # accurate
                result = {
                    "mode": mode,
                    "execution_time": "4.8s",
                    "steps": 8,
                    "accuracy": "excellent",
                    "description": "Deep analysis with comprehensive insights"
                }
            
            print(f"{mode.upper()} Mode:")
            print(f"  Time: {result['execution_time']}")
            print(f"  Steps: {result['steps']}")
            print(f"  Accuracy: {result['accuracy']}")
            print(f"  Description: {result['description']}\n")
    
    def run_all_examples(self, logger):
        """Run all basic examples."""
        logger.log_section("CUGA Basic Usage Examples")
        
        print("\n" + "="*60)
        print("CUGA Basic Usage Examples")
        print("="*60)
        
        logger.log_section("Example 1: Simple Task")
        result1 = self.example_1_simple_task()
        logger.log_result(result1)
        
        logger.log_section("Example 2: Task with Parameters")
        result2 = self.example_2_with_parameters()
        logger.log_result(result2)
        
        logger.log_section("Example 3: Error Handling")
        result3 = self.example_3_error_handling()
        logger.log_result(result3)
        
        logger.log_section("Example 4: Multi-Step Task")
        result4 = self.example_4_multi_step_task()
        logger.log_result(result4)
        
        logger.log_section("Example 5: Mode Comparison")
        self.example_5_mode_comparison()
        
        print("\n" + "="*60)
        print("Summary")
        print("="*60)
        print(f"\nTotal examples executed: 5")
        print(f"Successful tasks: {sum(1 for r in self.results if r['status'] == 'success')}")
        print(f"Failed tasks: {sum(1 for r in self.results if r['status'] == 'error')}")
        
        logger.log_section("Summary")
        logger.log_text(f"Total examples executed: 5")
        logger.log_text(f"Successful tasks: {sum(1 for r in self.results if r['status'] == 'success')}")
        logger.log_text(f"Failed tasks: {sum(1 for r in self.results if r['status'] == 'error')}")
        
        print("\n✓ All basic examples completed!")
        print("\nNext steps:")
        print("- Check out advanced_usage.py for more complex scenarios")
        print("- Explore tool_integration.py for custom tool examples")
        print("- See the agents/ directory for specialized agent implementations")


def main():
    """Main entry point."""
    logger = create_logger("basic_usage")
    examples = BasicCUGAExample()
    examples.run_all_examples(logger)
    logger.finalize()
    print(f"\n[Output saved to: {logger.get_filepath()}]")


if __name__ == "__main__":
    main()

# Made with Bob
