from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Annotated, List
from datetime import date

class PreferenceWeights(BaseModel):
    budget: float = Field(default=0.5, ge=0.0, le=1.0)
    culture: float = Field(default=0.5, ge=0.0, le=1.0)
    adventure: float = Field(default=0.5, ge=0.0, le=1.0)
    relaxation: float = Field(default=0.5, ge=0.0, le=1.0)
    nightlife: float = Field(default=0.5, ge=0.0, le=1.0)
    nature: float = Field(default=0.5, ge=0.0, le=1.0)
    local_experiences: float = Field(default=0.5, ge=0.0, le=1.0)
    personal_privacy: float = Field(default=0.5, ge=0.0, le=1.0)
    secluded_remote: float = Field(default=0.5, ge=0.0, le=1.0)
    culinary: float = Field(default=0.5, ge=0.0, le=1.0)
    family_friendly: float = Field(default=0.5, ge=0.0, le=1.0)
    walkability_transit: float = Field(default=0.5, ge=0.0, le=1.0)
    direct_flights_only: float = Field(default=0.5, ge=0.0, le=1.0)
    weekend_departure: float = Field(default=0.5, ge=0.0, le=1.0)
    convenient_departure_time: float = Field(default=0.5, ge=0.0, le=1.0)

    def to_vector(self) -> List[float]:
        """Returns deterministic 15-dimensional numerical float vector."""
        return [
            self.budget,
            self.culture,
            self.adventure,
            self.relaxation,
            self.nightlife,
            self.nature,
            self.local_experiences,
            self.personal_privacy,
            self.secluded_remote,
            self.culinary,
            self.family_friendly,
            self.walkability_transit,
            self.direct_flights_only,
            self.weekend_departure,
            self.convenient_departure_time
        ]

class UserPreferenceSchema(BaseModel):
    raw_query: str
    max_budget: float | None = None
    duration_days: int | None = Field(default=None, ge=1,le=60)
    tolerance_days: int = Field(default=0, ge=0, le=7)
    start_date: date | None = None
    end_date: date | None = None
    target_country: str | None = None
    target_region: str | None = None
    weights: PreferenceWeights = Field(default_factory=PreferenceWeights)

    @field_validator("raw_query")
    @classmethod
    def validate_raw_query(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("raw query cannot be empty")
        return cleaned

    @model_validator(mode="after")
    def validate_date_range(self) -> "UserPreferenceSchema":
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be on or after start_date")
        return self

class DestinationVibeVector(BaseModel):
    destination_id: str
    destination_name: str
    vibe_scores: PreferenceWeights

class ScoredDestination(BaseModel):
    destination_id: str
    destination_name: str
    score: float = Field(..., le=0, ge=1)
    tradeoff_summary: str