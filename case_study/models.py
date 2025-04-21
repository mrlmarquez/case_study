from typing import List
from pydantic import BaseModel, Field


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
