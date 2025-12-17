#!/usr/bin/env python3
"""
CUGA API Agent

Demonstrates API-focused agent implementation for executing tasks
that primarily involve API calls and data processing.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class CUGAAPIAgent:
    """
    API-focused CUGA agent implementation.
    
    This agent specializes in:
    - REST API interactions
    - Data retrieval and processing
    - Multi-step API workflows
    - Result aggregation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize API agent.
        
        Args:
            config: Agent configuration dictionary
        """
        self.config = config or self._load_default_config()
        self.tools = self._initialize_tools()
        self.execution_history = []
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "mode": "api",
            "reasoning_mode": "balanced",
            "max_iterations": 20,
            "timeout": 300,
            "enable_caching": True
        }
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """
        Initialize API tools.
        
        In a real implementation, this would:
        1. Load OpenAPI specifications
        2. Initialize API clients
        3. Set up authentication
        4. Configure rate limiting
        """
        return {
            "crm_api": {
                "base_url": "https://api.example.com/crm",
                "endpoints": ["accounts", "contacts", "opportunities"],
                "auth": "bearer_token"
            },
            "sales_api": {
                "base_url": "https://api.example.com/sales",
                "endpoints": ["revenue", "forecasts", "analytics"],
                "auth": "api_key"
            }
        }
    
    def execute(self, task: str) -> Dict[str, Any]:
        """
        Execute an API-focused task.
        
        Args:
            task: Natural language task description
            
        Returns:
            Execution result with data and metadata
        """
        print(f"\n{'='*60}")
        print(f"API Agent: Executing Task")
        print(f"{'='*60}")
        print(f"Task: {task}")
        print(f"Mode: {self.config['reasoning_mode']}")
        
        # Simulate task execution
        result = self._simulate_execution(task)
        
        # Store in history
        self.execution_history.append({
            "task": task,
            "result": result,
            "timestamp": "2024-12-17T14:00:00Z"
        })
        
        return result
    
    def _simulate_execution(self, task: str) -> Dict[str, Any]:
        """
        Simulate task execution.
        
        In a real implementation, this would:
        1. Parse the task
        2. Plan API calls
        3. Execute calls in sequence
        4. Process and aggregate results
        """
        # Example: CRM query
        if "account" in task.lower():
            return self._handle_account_query(task)
        
        # Example: Sales query
        elif "revenue" in task.lower() or "sales" in task.lower():
            return self._handle_sales_query(task)
        
        # Default response
        return {
            "status": "success",
            "message": "Task executed successfully",
            "data": {},
            "execution_time": "1.5s"
        }
    
    def _handle_account_query(self, task: str) -> Dict[str, Any]:
        """Handle account-related queries."""
        print("\nStep 1: Analyzing task requirements")
        print("Step 2: Calling CRM API - GET /accounts")
        print("Step 3: Processing response data")
        print("Step 4: Formatting results")
        
        return {
            "status": "success",
            "task_type": "account_query",
            "api_calls": [
                {
                    "endpoint": "/crm/accounts",
                    "method": "GET",
                    "params": {"sort": "revenue", "order": "desc"},
                    "status": 200
                }
            ],
            "data": {
                "accounts": [
                    {
                        "id": 1,
                        "name": "Global Solutions",
                        "revenue": 2000000,
                        "industry": "Technology"
                    },
                    {
                        "id": 2,
                        "name": "Acme Corp",
                        "revenue": 1500000,
                        "industry": "Manufacturing"
                    }
                ],
                "total_count": 2
            },
            "execution_time": "1.8s",
            "mode": self.config['reasoning_mode']
        }
    
    def _handle_sales_query(self, task: str) -> Dict[str, Any]:
        """Handle sales-related queries."""
        print("\nStep 1: Analyzing sales metrics request")
        print("Step 2: Calling Sales API - GET /revenue")
        print("Step 3: Aggregating data")
        print("Step 4: Calculating insights")
        
        return {
            "status": "success",
            "task_type": "sales_query",
            "api_calls": [
                {
                    "endpoint": "/sales/revenue",
                    "method": "GET",
                    "params": {"period": "Q4", "year": 2024},
                    "status": 200
                }
            ],
            "data": {
                "total_revenue": 5500000,
                "growth_rate": 15.3,
                "top_products": [
                    {"name": "Product A", "revenue": 2000000},
                    {"name": "Product B", "revenue": 1800000}
                ]
            },
            "execution_time": "2.1s",
            "mode": self.config['reasoning_mode']
        }
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history = []


def demo_api_agent():
    """Demonstrate API agent capabilities."""
    print("\n" + "="*60)
    print("CUGA API Agent Demonstration")
    print("="*60)
    
    # Initialize agent
    agent = CUGAAPIAgent()
    
    # Example 1: Account query
    print("\n\nExample 1: Account Query")
    print("-" * 60)
    result1 = agent.execute("Get top 2 accounts by revenue")
    print(f"\n✓ Result: {result1['status']}")
    print(f"  Accounts found: {result1['data']['total_count']}")
    print(f"  Execution time: {result1['execution_time']}")
    
    # Example 2: Sales query
    print("\n\nExample 2: Sales Query")
    print("-" * 60)
    result2 = agent.execute("Show Q4 2024 revenue breakdown")
    print(f"\n✓ Result: {result2['status']}")
    print(f"  Total revenue: ${result2['data']['total_revenue']:,}")
    print(f"  Growth rate: {result2['data']['growth_rate']}%")
    print(f"  Execution time: {result2['execution_time']}")
    
    # Show history
    print("\n\nExecution History")
    print("-" * 60)
    history = agent.get_execution_history()
    print(f"Total tasks executed: {len(history)}")
    for i, entry in enumerate(history, 1):
        print(f"\n{i}. {entry['task']}")
        print(f"   Status: {entry['result']['status']}")
        print(f"   Time: {entry['result']['execution_time']}")
    
    print("\n" + "="*60)
    print("✓ API Agent demonstration completed!")
    print("="*60)


if __name__ == "__main__":
    demo_api_agent()

# Made with Bob
