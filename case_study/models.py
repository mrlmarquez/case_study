from typing import List, Annotated
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from uuid import uuid4

import operator
from typing_extensions import TypedDict


class ContractLeaseContent(Document):
    def __init__(content, document_title):
        super().__init__(
            page_content=content,
            metadata={"document_title": document_title},
            id=uuid4(),
        )


class LegalEntities(BaseModel):
    end_date: List[str] = Field(default=[""], description="The end date of the lease.")
    leased_space: List[str] = Field(
        default=[""], description="Description of the space that is being leased."
    )
    lessee: List[str] = Field(
        default=[""], description="The lessee's name (and possibly address)."
    )
    lessor: List[str] = Field(
        default=[""], description="The lessor's name (and possibly address)."
    )
    signing_date: List[str] = Field(
        default=[""], description="The date the contract was signed."
    )
    start_date: List[str] = Field(
        default=[""], description="The start date of the lease."
    )
    term_of_payment: List[str] = Field(
        default=[""], description="Description of the payment terms."
    )
    designated_use: List[str] = Field(
        default=[""], description="Designated use of the property being leased."
    )
    extension_period: List[str] = Field(
        default=[""], description="Description of the extension options for the lease."
    )
    expiration_date_of_lease: List[str] = Field(
        default=[""], description="The expiration date of the lease."
    )


class RuleStep(BaseModel):
    rule: str
    explanation: str

    def __str__(self):
        return f"""Rule: {self.rule}\n\nExplanation of the rule: {self.explanation}"""


class ApplicationStep(BaseModel):
    related_clauses: List[str]
    application_explanation: str

    def __str__(self):
        related_clauses_str = "\n\n".join(self.related_clauses)
        return f"""Related Clauses: {related_clauses_str}\n\nExplanation of the application: {self.application_explanation}"""


class GraphState(TypedDict):
    """
    Graph state is a dictionary that contains information we want to propagate to, and modify in, each graph node.
    """

    active_clause: str
    incoming_clause: str
    issue: str  # User question
    conclusion: str
    is_conclusion_found: bool
    loop_step: Annotated[int, operator.add]
    rule_step: List[RuleStep]
    application_step: List[ApplicationStep]
