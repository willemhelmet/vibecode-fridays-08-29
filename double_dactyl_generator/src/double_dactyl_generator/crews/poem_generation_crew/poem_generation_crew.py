from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ...tools.reference_reader_tool import ReferenceReaderTool

@CrewBase
class PoemGenerationCrew:
    """PoemGenerationCrew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def poet(self) -> Agent:
        return Agent(
            config=self.agents_config["poet"],
            tools=[ReferenceReaderTool()],
        )

    @task
    def create_poem(self) -> Task:
        return Task(
            config=self.tasks_config["create_poem_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PoemGenerationCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
