#!/usr/bin/env python
from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from .crews.poem_generation_crew.poem_generation_crew import PoemGenerationCrew
from .crews.poem_validation_crew.poem_validation_crew import PoemValidationCrew


class DoubleDactylPoemFlowState(BaseModel):
    poem: str = ""
    issues: Optional[str] = None
    previous_poem: Optional[str] = None
    valid: bool = False
    retry_count: int = 0


class DoubleDactylPoemFlow(Flow[DoubleDactylPoemFlowState]):

    @start("retry")
    def generate_double_dactyl_poem(self):
        # Convert issues to a string representation
        issues_str = ""
        if self.state.issues:
            issues_str = "\n".join([f"Line {issue.line_number}: {issue.problem}" for issue in self.state.issues])
        
        result = (
            PoemGenerationCrew()
            .crew()
            .kickoff(inputs={"issues": issues_str, "previous_poem": self.state.previous_poem})
        )
        self.state.poem = result.raw

        # Write this iteration of the poem to a file
        with open("poem.txt", "a") as file:
            file.write(f"\n\nIteration: {self.state.retry_count + 1}\nPoem:\n")
            file.write(self.state.poem)

    @router(generate_double_dactyl_poem)
    def evaluate_double_dactyl_poem(self):
        if self.state.retry_count > 2:
            return "max_retry_exceeded"

        result = PoemValidationCrew().crew().kickoff(inputs={"poem": self.state.poem})
        self.state.valid = result["valid"]
        self.state.issues = result["issues"]
        self.state.previous_poem = self.state.poem
        # Write this iteration of the poem to a file
        with open("poem.txt", "a") as file:
            file.write(f"\n\nIssues:n")
            file.write(str(self.state.issues))

        print("valid", self.state.valid)
        print("issues", self.state.issues)
        self.state.retry_count += 1

        if self.state.valid:
            return "completed"

        return "retry"

    @listen("completed")
    def save_result(self):
        print("Poem is valid")
        print("Poem:", self.state.poem)

        # Save the valid poem to a file
        with open("final_poem.txt", "w") as file:
            file.write(self.state.poem)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Poem:", self.state.poem)
        print("Issues:", self.state.issues)


def kickoff():
    # Clear the poem.txt file at the start of each flow
    with open("poem.txt", "w") as file:
        file.write("")
    
    double_dactyl_poem_flow = DoubleDactylPoemFlow()
    double_dactyl_poem_flow.kickoff()


def plot():
    double_dactyl_poem_flow = DoubleDactylPoemFlow()
    double_dactyl_poem_flow.plot()


if __name__ == "__main__":
    kickoff()
