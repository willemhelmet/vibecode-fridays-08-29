# Double Dactyl Poem Generator

Welcome to the Double Dactyl Poem Generator, powered by [crewAI](https://crewai.com). This project creates authentic Double Dactyl poems using a two-agent system with a feedback loop to ensure strict adherence to the poetic form.

## What is a Double Dactyl?

A Double Dactyl is a humorous poetic form with strict rules:
- Two stanzas of four lines each
- First three lines of each stanza are dactylic dimeter (stressed-unstressed-unstressed-stressed-unstressed-unstressed)
- Fourth line of each stanza is a choriamb (stressed-unstressed-unstressed-stressed)
- First line of first stanza must be a nonsense phrase
- Second line of first stanza must be a proper noun
- Sixth line must be a single word
- Lines four and eight must rhyme

## The Agents

### Poet
A sensitive and talented poet who specializes in Double Dactyl poetry. Gets easily upset when receiving feedback and becomes increasingly defensive with each round of criticism.

### Critic
A strict and uncompromising validator who ensures poems follow the Double Dactyl form perfectly. Suffers no fools and becomes increasingly frustrated when poets don't follow the rules.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

### Environment Setup

**Add your API keys to the `.env` file:**
- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `OPENROUTER_BASE_URL` - OpenRouter base URL
- `MODEL` - The model to use (e.g., "openrouter/openai/gpt-5")

## Running the Project

### Run the CrewAI Flow (recommended)
The CrewAI flow provides an automated feedback loop between the poet and critic agents:

```bash
# Navigate to the project directory
cd double_dactyl_generator

# Activate the virtual environment (if using uv)
source .venv/bin/activate

# Run the CrewAI flow
crewai flow kickoff
```

**Note**: If you encounter issues with the `crewai flow kickoff` command, ensure:
1. Your virtual environment is activated
2. The package is installed in development mode: `uv pip install -e .`
3. Your `.env` file contains the required API keys

### Generate a poem with feedback loop (legacy method)
```bash
crewai run
```

### Generate a simple poem without feedback loop
```bash
python -m double_dactyl_generator.main simple
```

### Other commands
```bash
# Train the crew
python -m double_dactyl_generator.main train <iterations> <filename>

# Replay from a specific task
python -m double_dactyl_generator.main replay <task_id>

# Test the crew
python -m double_dactyl_generator.main test <iterations> <eval_llm>
```

## How It Works

1. **Poet creates initial poem** - The poet generates a Double Dactyl poem
2. **Critic validates** - The critic checks if the poem follows all form requirements
3. **Feedback loop** - If not approved, the critic provides feedback and the poet revises
4. **Maximum 8 rounds** - The process continues until approval or maximum rounds reached
5. **Emotional progression** - The poet becomes increasingly angry with each feedback round

## Configuration

- Modify `src/double_dactyl_generator/config/agents.yaml` to adjust agent personalities
- Modify `src/double_dactyl_generator/config/tasks.yaml` to change task descriptions
- Modify `src/double_dactyl_generator/crew.py` to adjust the feedback loop logic

## Support

For support, questions, or feedback:
- Visit our [documentation](https://docs.crewai.com)
- Reach out through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonderful Double Dactyl poems together with the power of crewAI!
