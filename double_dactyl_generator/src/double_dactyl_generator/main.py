#!/usr/bin/env python
import sys
import warnings

from double_dactyl_generator.crew import DoubleDactylGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Double Dactyl poem generator.
    """
    try:
        generator = DoubleDactylGenerator()
        result = generator.generate_poem_with_feedback(max_feedback_rounds=8)
        print("\n" + "="*50)
        print(result)
        print("="*50)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run_simple():
    """
    Run a simple version without the feedback loop.
    """
    try:
        result = DoubleDactylGenerator().crew().kickoff()
        print("\n" + "="*50)
        print("CREW EXECUTION COMPLETED")
        print("="*50)
        print(f"Result: {result}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        generator = DoubleDactylGenerator()
        generator.crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2]
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DoubleDactylGenerator().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        generator = DoubleDactylGenerator()
        generator.crew().test(
            n_iterations=int(sys.argv[1]), 
            eval_llm=sys.argv[2]
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        elif command == "simple":
            run_simple()
        else:
            print("Unknown command. Available commands: train, replay, test, simple")
    else:
        run()
