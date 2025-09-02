from typing import Optional, List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from ...tools.reference_reader_tool import ReferenceReaderTool

class Issue(BaseModel):
    line_number: int
    problem: str

class PoemValidationResult(BaseModel):
    valid: bool
    issues: List[Issue] = []

@CrewBase
class PoemValidationCrew:
    """PoemValidationCrew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def critic(self) -> Agent:
        return Agent(
            config=self.agents_config["critic"],
            tools=[ReferenceReaderTool()],
        )

    @task
    def validate_poem(self) -> Task:
        return Task(
            config=self.tasks_config["validate_poem_task"],
            output_pydantic=PoemValidationResult,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PoemValidationCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
