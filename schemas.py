from pydantic import BaseModel, Field
from typing import List

class Goal(BaseModel):
    metric: str = Field(description="The quantifiable metric or target, e.g., Page load time under 1s")
    target: str = Field(description="The specific target goal")

class UserStory(BaseModel):
    id: str = Field(description="Unique identifier like US-001")
    as_a: str = Field(description="The user persona or role")
    i_want: str = Field(description="The action or feature the user wants")
    so_that: str = Field(description="The benefit or value the user gains")
    acceptance_criteria: List[str] = Field(description="Given-When-Then testable conditions")

class Scope(BaseModel):
    in_scope: List[str] = Field(description="Features or functionalities included in this version")
    out_of_scope: List[str] = Field(description="Explicitly excluded features or functionalities to prevent scope creep")

class ProductRequirementsDocument(BaseModel):
    project_title: str = Field(description="Clear title of the product or feature")
    problem_statement: str = Field(description="The core user and business problem being solved")
    target_audience: str = Field(description="Who the product is for, including why they need it")
    goals_and_kpis: List[Goal] 
    user_stories: List[UserStory] 
    technical_considerations: List[str] = Field(description="Tech stack, architecture, APIs, security, and performance considerations")
    scope: Scope