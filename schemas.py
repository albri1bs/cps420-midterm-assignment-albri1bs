from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class Category(str, Enum):
    electronics = "electronics"
    clothing    = "clothing"
    accessories = "accessories"
    books       = "books"
    keys        = "keys"
    wallet      = "wallet"
    other       = "other"

class Status(str, Enum):
    lost    = "lost"
    found   = "found"
    claimed = "claimed"

class ClaimIn(BaseModel):
    claimant_name:  str = Field(..., min_length=1, max_length=100)
    claimant_email: str = Field(..., min_length=5, max_length=150)
    description:    str = Field(..., min_length=10, max_length=1000)
    approved:       bool = False

class ClaimOut(BaseModel):
    id:             int
    claimant_name:  str
    claimant_email: str
    description:    str
    approved:       bool
    created:        datetime

    model_config = {"from_attributes": True}

class ItemIn(BaseModel):
    name:        str      = Field(..., min_length=1, max_length=200)
    description: str      = Field(default="", max_length=1000)
    category:    Category = Category.other
    location:    str      = Field(..., min_length=1, max_length=200)
    status:      Status   = Status.lost
    resolved:    bool     = False
    date_lost:   datetime

class ItemOut(BaseModel):
    id:          int
    name:        str
    description: str
    category:    Category
    location:    str
    status:      Status
    resolved:    bool
    date_lost:   datetime
    created:     datetime
    claims:      list[ClaimOut] = []

    model_config = {"from_attributes": True}

class ItemStats(BaseModel):
    item_id:      int
    name:         str
    total_claims: int
    approved:     int
    resolved:     bool