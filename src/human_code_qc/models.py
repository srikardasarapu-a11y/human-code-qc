from pydantic import BaseModel, Field

class ValidationStatus(BaseModel):
    syntaxValid: bool = True
    utf8Valid: bool = True

class ProblemContext(BaseModel):
    problemId: str = ""
    title: str = ""
    problemStatement: str = ""

class MetadataRecord(BaseModel):
    solutionId: str
    problemId: str
    language: str
    problem: ProblemContext = Field(default_factory=ProblemContext)
    validation: ValidationStatus = Field(default_factory=ValidationStatus)
