#!/usr/bin/env python3
"""
Custom CUGA Tools

Demonstrates how to create custom LangChain tools for CUGA integration.
"""

import sys
from pathlib import Path
from typing import Optional, Type, Any
from pydantic import BaseModel, Field

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import output logger
from src.utils.output_logger import create_logger


class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(description="Mathematical expression to evaluate")


class CalculatorTool:
    """
    Custom calculator tool for mathematical operations.
    
    This demonstrates:
    - Tool input validation
    - Safe expression evaluation
    - Error handling
    """
    
    name: str = "calculator"
    description: str = "Evaluate mathematical expressions safely"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """
        Execute the calculator tool.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Result as string
        """
        try:
            # Safe evaluation (in production, use a proper math parser)
            # This is simplified for demonstration
            allowed_chars = set("0123456789+-*/()., ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """Async version of the tool."""
        return self._run(expression)


class SentimentAnalyzerInput(BaseModel):
    """Input schema for sentiment analyzer tool."""
    text: str = Field(description="Text to analyze for sentiment")


class SentimentAnalyzerTool:
    """
    Custom sentiment analysis tool.
    
    This demonstrates:
    - Text processing
    - Sentiment classification
    - Confidence scoring
    """
    
    name: str = "sentiment_analyzer"
    description: str = "Analyze sentiment of text (positive, negative, neutral)"
    args_schema: Type[BaseModel] = SentimentAnalyzerInput
    
    def _run(self, text: str) -> str:
        """
        Execute sentiment analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis result
        """
        # Simplified sentiment analysis (in production, use proper NLP)
        text_lower = text.lower()
        
        positive_words = ["good", "great", "excellent", "happy", "love", "best"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return f"Sentiment: {sentiment} (confidence: {confidence:.2f})"
    
    async def _arun(self, text: str) -> str:
        """Async version of the tool."""
        return self._run(text)


class DataProcessorInput(BaseModel):
    """Input schema for data processor tool."""
    data: str = Field(description="Data to process (JSON string)")
    operation: str = Field(description="Operation to perform (filter, sort, aggregate)")


class DataProcessorTool:
    """
    Custom data processing tool.
    
    This demonstrates:
    - Data transformation
    - Multiple operations
    - Structured output
    """
    
    name: str = "data_processor"
    description: str = "Process and transform data with various operations"
    args_schema: Type[BaseModel] = DataProcessorInput
    
    def _run(self, data: str, operation: str) -> str:
        """
        Execute data processing.
        
        Args:
            data: JSON string of data
            operation: Operation to perform
            
        Returns:
            Processed data result
        """
        import json
        
        try:
            # Parse input data
            data_obj = json.loads(data)
            
            if operation == "filter":
                # Example: filter items with value > 100
                if isinstance(data_obj, list):
                    result = [item for item in data_obj 
                             if isinstance(item, dict) and item.get("value", 0) > 100]
                else:
                    result = data_obj
                    
            elif operation == "sort":
                # Example: sort by value
                if isinstance(data_obj, list):
                    result = sorted(data_obj, 
                                  key=lambda x: x.get("value", 0) if isinstance(x, dict) else 0,
                                  reverse=True)
                else:
                    result = data_obj
                    
            elif operation == "aggregate":
                # Example: sum all values
                if isinstance(data_obj, list):
                    total = sum(item.get("value", 0) for item in data_obj 
                              if isinstance(item, dict))
                    result = {"total": total, "count": len(data_obj)}
                else:
                    result = data_obj
            else:
                return f"Error: Unknown operation '{operation}'"
            
            return json.dumps(result, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON data"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, data: str, operation: str) -> str:
        """Async version of the tool."""
        return self._run(data, operation)


def demo_custom_tools():
    """Demonstrate custom tools."""
    logger = create_logger("custom_tools")
    
    logger.log_section("CUGA Custom Tools Demonstration")
    logger.log_text("Testing custom LangChain tools for CUGA integration")
    
    print("\n" + "="*60)
    print("CUGA Custom Tools Demonstration")
    print("="*60)
    
    # Calculator Tool
    logger.log_section("Example 1: Calculator Tool")
    print("\n\nExample 1: Calculator Tool")
    print("-" * 60)
    calc = CalculatorTool()
    expression = "(10 + 5) * 2"
    result = calc._run(expression)
    print(f"Expression: {expression}")
    print(f"Result: {result}")
    logger.log_text(f"**Expression:** `{expression}`")
    logger.log_text(f"**Result:** {result}")
    
    # Sentiment Analyzer Tool
    logger.log_section("Example 2: Sentiment Analyzer Tool")
    print("\n\nExample 2: Sentiment Analyzer Tool")
    print("-" * 60)
    sentiment = SentimentAnalyzerTool()
    text = "This product is excellent and I love it!"
    result = sentiment._run(text)
    print(f"Text: {text}")
    print(f"Analysis: {result}")
    logger.log_text(f"**Text:** {text}")
    logger.log_text(f"**Analysis:** {result}")
    
    # Data Processor Tool
    logger.log_section("Example 3: Data Processor Tool")
    print("\n\nExample 3: Data Processor Tool")
    print("-" * 60)
    processor = DataProcessorTool()
    data = '[{"name": "A", "value": 150}, {"name": "B", "value": 80}, {"name": "C", "value": 200}]'
    
    print("Original data:")
    print(data)
    logger.log_text("**Original data:**")
    logger.log_code(data, "json")
    
    print("\nOperation: filter (value > 100)")
    result_filter = processor._run(data, "filter")
    print(result_filter)
    logger.log_text("**Operation:** filter (value > 100)")
    logger.log_code(result_filter, "json")
    
    print("\nOperation: aggregate")
    result_agg = processor._run(data, "aggregate")
    print(result_agg)
    logger.log_text("**Operation:** aggregate")
    logger.log_code(result_agg, "json")
    
    print("\n" + "="*60)
    print("✓ Custom tools demonstration completed!")
    print("="*60)
    
    logger.log_section("Summary")
    logger.log_text("✓ All 3 custom tools tested successfully")
    logger.log_list([
        "Calculator Tool - Mathematical expressions",
        "Sentiment Analyzer Tool - Text sentiment analysis",
        "Data Processor Tool - Data transformation operations"
    ])
    logger.finalize()
    print(f"\n[Output saved to: {logger.get_filepath()}]")


if __name__ == "__main__":
    demo_custom_tools()

# Made with Bob
