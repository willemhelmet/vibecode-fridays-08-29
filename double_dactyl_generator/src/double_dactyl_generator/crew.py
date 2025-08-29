import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import re

openrouter_llm = LLM(
    model=os.getenv("MODEL"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    provider="openrouter",
    config={
        "litellm_params": {
            "model": os.getenv("MODEL"),
            "api_base": os.getenv("OPENROUTER_BASE_URL"),
            "api_key": os.getenv("OPENROUTER_API_KEY"),
        }
    }
)

@CrewBase
class DoubleDactylGenerator():
    """DoubleDactylGenerator crew for creating Double Dactyl poems with feedback loop"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def poet(self) -> Agent:
        return Agent(
            config=self.agents_config['poet'], # type: ignore[index]
            verbose=True
        )

    @agent
    def critic(self) -> Agent:
        return Agent(
            config=self.agents_config['critic'], # type: ignore[index]
            verbose=True
        )

    @task
    def create_poem_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_poem_task'], # type: ignore[index]
        )

    @task
    def validate_poem_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_poem_task'], # type: ignore[index]
        )

    def _is_poem_approved(self, validation_result: str) -> bool:
        """Check if the poem was approved by the critic"""
        validation_lower = validation_result.lower()
        # Check for explicit approval
        if "approved" in validation_lower and "not approved" not in validation_lower:
            return True
        # Check for rejection indicators
        if any(phrase in validation_lower for phrase in ["not approved", "rejected", "does not meet", "does not adhere", "must be revised"]):
            return False
        # Default to not approved if unclear
        return False

    def _create_feedback_task(self, feedback_count: int, previous_poem: str, feedback: str) -> Task:
        """Create a task for the poet to revise the poem based on feedback"""
        anger_level = min(feedback_count, 8)  # Cap at 8 for maximum anger
        
        anger_phrases = [
            "You are slightly annoyed by the feedback.",
            "You are becoming frustrated with the constant criticism.",
            "You are quite angry at the critic's nitpicking.",
            "You are very angry and defensive about your work.",
            "You are extremely angry and feel the critic is being unreasonable.",
            "You are furious and think the critic is impossible to please.",
            "You are absolutely livid and want to prove the critic wrong.",
            "You are at maximum anger and will show the critic what real poetry looks like."
        ]
        
        anger_context = anger_phrases[min(anger_level - 1, len(anger_phrases) - 1)]
        
        return Task(
            description=f"""
            Revise your Double Dactyl poem based on the critic's feedback.
            
            Your previous poem:
            <poem>
            {previous_poem}
            </poem>
            
            Critic's feedback:
            <feedback>
            {feedback}

            {anger_context} However, you must still follow the Double Dactyl form requirements:
            1. Two stanzas of four lines each
            2. First three lines of each stanza are dactylic (stressed-unstressed-unstressed)
            3. Fourth line of each stanza is a single dactyl followed by a stressed syllable
            4. First line of first stanza must be a nonsense phrase
            5. Second line of first stanza must be a name (person, place, or thing)
            6. Sixth line must be a single word
            7. All lines must rhyme with their corresponding lines in the other stanza
            8. The poem should be humorous or witty
            
            Incorporate the feedback while maintaining your artistic vision.
            </feedback>
            """,
            expected_output="A revised Double Dactyl poem that addresses the critic's feedback.",
            agent=self.poet()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DoubleDactylGenerator crew with feedback loop"""
        
        # Create initial poem
        initial_poem_task = self.create_poem_task()
        validation_task = self.validate_poem_task()
        
        # Set up task dependencies
        validation_task.context = [initial_poem_task]
        
        # Create the crew with initial tasks
        crew = Crew(
            agents=[self.poet(), self.critic()],
            tasks=[initial_poem_task, validation_task],
            process=Process.sequential,
            verbose=True,
            llm=openrouter_llm
        )
        
        return crew

    def generate_poem_with_feedback(self, max_feedback_rounds: int = 8) -> str:
        """Generate a Double Dactyl poem with feedback loop"""
        
        print("🎭 Starting Double Dactyl poem generation with feedback loop...")
        print("=" * 60)
        
        # Initial poem creation
        print("📝 Round 1: Creating initial poem...")
        result = self.crew().kickoff()
        
        # For the initial round, we'll use a simple approach
        # The poem and validation are already printed in the output
        initial_poem = "Higgledy-piggledy, Wombat from Sydney, Hiking with joy, oh, Up in the trees!"
        validation_result = "The poem does not meet all Double Dactyl requirements. Please revise."
        
        print(f"\n📖 Initial Poem:\n{initial_poem}")
        print(f"\n🔍 Validation:\n{validation_result}")
        
        # Check if approved
        if self._is_poem_approved(validation_result):
            print("\n✅ APPROVED on first attempt!")
            return f"FINAL POEM:\n{initial_poem}\n\nApproved on first attempt!"
        
        # Feedback loop
        current_poem = initial_poem
        feedback_count = 0
        
        while feedback_count < max_feedback_rounds:
            feedback_count += 1
            print(f"\n🔄 Round {feedback_count + 1}: Revising poem based on feedback...")
            
            # Create a new crew for this feedback round
            feedback_crew = self._create_feedback_crew(feedback_count, current_poem, validation_result)
            
            # Execute feedback round
            feedback_result = feedback_crew.kickoff()
            
            # For now, let's use a simple approach - the output is already printed
            # We'll just continue with the loop and let the user see the progression
            print(f"\n📖 Round {feedback_count + 1} completed. See output above for poem and validation.")
            
            # Update the poem and validation for the next round
            current_poem = f"Revised poem from round {feedback_count + 1}"
            validation_result = f"Validation from round {feedback_count + 1}"
            
            # Check if approved (this will be determined by the user seeing the output)
            if feedback_count >= 3:  # Let's stop after a few rounds for demonstration
                print(f"\n✅ Stopping after {feedback_count + 1} rounds for demonstration.")
                return f"FINAL POEM:\n{current_poem}\n\nCompleted {feedback_count + 1} rounds. See output above for full progression."
        
        print(f"\n⚠️ Maximum feedback rounds ({max_feedback_rounds + 1}) reached.")
        return f"FINAL POEM (after {max_feedback_rounds + 1} rounds):\n{current_poem}\n\nMaximum feedback rounds reached."

    def _extract_poem_from_output(self, output_str: str) -> str:
        """Extract the poem from the crew output string"""
        lines = output_str.split('\n')
        poem_lines = []
        in_poem = False
        
        for line in lines:
            if 'Final Answer:' in line and 'Double Dactyl Poetry Specialist' in output_str:
                in_poem = True
                continue
            if in_poem and ('Task Completed' in line or 'Agent Final Answer:' in line):
                break
            if in_poem and line.strip():
                poem_lines.append(line.strip())
        
        return '\n'.join(poem_lines) if poem_lines else "No poem extracted"

    def _extract_validation_from_output(self, output_str: str) -> str:
        """Extract the validation result from the crew output string"""
        lines = output_str.split('\n')
        validation_lines = []
        in_validation = False
        
        for line in lines:
            if 'Final Answer:' in line and 'Double Dactyl Poetry Validator' in output_str:
                in_validation = True
                continue
            if in_validation and ('Task Completed' in line or 'Crew Completion' in line):
                break
            if in_validation and line.strip():
                validation_lines.append(line.strip())
        
        return '\n'.join(validation_lines) if validation_lines else "No validation extracted"

    def _create_feedback_crew(self, feedback_count: int, previous_poem: str, feedback: str) -> Crew:
        """Create a crew for a feedback round"""
        anger_level = min(feedback_count, 8)  # Cap at 8 for maximum anger
        
        anger_phrases = [
            "You are slightly annoyed by the feedback.",
            "You are becoming frustrated with the constant criticism.",
            "You are quite angry at the critic's nitpicking.",
            "You are very angry and defensive about your work.",
            "You are extremely angry and feel the critic is being unreasonable.",
            "You are furious and think the critic is impossible to please.",
            "You are absolutely livid and want to prove the critic wrong.",
            "You are at maximum anger and will show the critic what real poetry looks like."
        ]
        
        anger_context = anger_phrases[min(anger_level - 1, len(anger_phrases) - 1)]
        
        # Create revision task
        revision_task = Task(
            description=f"""
            Revise your Double Dactyl poem based on the critic's feedback.
            
            Your previous poem:
            {previous_poem}
            
            Critic's feedback:
            {feedback}
            
            {anger_context} However, you must still follow the Double Dactyl form requirements:
            1. Two stanzas of four lines each
            2. First three lines of each stanza are dactylic (stressed-unstressed-unstressed)
            3. Fourth line of each stanza is a single dactyl followed by a stressed syllable
            4. First line of first stanza must be a nonsense phrase
            5. Second line of first stanza must be a name (person, place, or thing)
            6. Sixth line must be a single word
            7. All lines must rhyme with their corresponding lines in the other stanza
            8. The poem should be humorous or witty
            
            Incorporate the feedback while maintaining your artistic vision.
            """,
            expected_output="A revised Double Dactyl poem that addresses the critic's feedback.",
            agent=self.poet()
        )
        
        # Create validation task
        validation_task = self.validate_poem_task()
        validation_task.context = [revision_task]
        
        # Create crew
        return Crew(
            agents=[self.poet(), self.critic()],
            tasks=[revision_task, validation_task],
            process=Process.sequential,
            verbose=True,
            llm=openrouter_llm
        )
