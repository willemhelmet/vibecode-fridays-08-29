from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class ReferenceReaderInput(BaseModel):
    """Input schema for ReferenceReaderTool."""
    file_path: str = Field(..., description="Path to the reference file to read")

class ReferenceReaderTool(BaseTool):
    name: str = "reference_reader_tool"
    description: str = "Reads reference files from the knowledge directory"
    
    def _run(self, file_path: str) -> str:
        """Read the content of a reference file."""
        try:
            # Construct full path relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            full_path = os.path.join(project_root, file_path)
            
            with open(full_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return f"Reference file {file_path} not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    args_schema: Type[BaseModel] = ReferenceReaderInput
