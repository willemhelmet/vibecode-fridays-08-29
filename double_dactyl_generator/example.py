#!/usr/bin/env python
"""
Example script for the Double Dactyl Poem Generator
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from double_dactyl_generator.crew import DoubleDactylGenerator

def main():
    """Run the Double Dactyl generator example"""
    
    # Check if environment variables are set
    required_vars = ['OPENROUTER_API_KEY', 'OPENROUTER_BASE_URL', 'MODEL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file:")
        print("OPENROUTER_API_KEY=your_openrouter_api_key_here")
        print("OPENROUTER_BASE_URL=https://openrouter.ai/api/v1")
        print("MODEL=anthropic/claude-3.5-sonnet")
        return
    
    print("🎭 Double Dactyl Poem Generator")
    print("=" * 40)
    
    try:
        # Create the generator
        generator = DoubleDactylGenerator()
        
        # Generate a poem with feedback loop
        print("Creating your Double Dactyl poem...")
        print("(This may take a few minutes with the feedback loop)")
        print()
        
        result = generator.generate_poem_with_feedback(max_feedback_rounds=8)
        
        print("\n" + "=" * 50)
        print("🎉 FINAL RESULT:")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure your API keys are correct and you have sufficient credits.")

if __name__ == "__main__":
    main()
