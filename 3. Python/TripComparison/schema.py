from pydantic import BaseModel, Field
from typing import Literal, Annotated, List
from datetime import date

class PreferenceWeights(BaseModel):
    budget: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Importance of affordability, low-cost accommodations, and budget-friendly travel over luxury."
    )
    culture: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for historical sites, museums, architecture, heritage, art galleries, and passive cultural sightseeing."
    )
    adventure: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for high-energy, thrill-seeking, extreme outdoor activities, and physically demanding exploration."
    )
    relaxation: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for downtime, beach lounging, spa treatments, slow-paced schedules, and stress-free rest."
    )
    nightlife: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for evening entertainment, bars, dance clubs, live music venues, and late-night dining."
    )
    nature: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for scenic natural landscapes, national parks, wildlife watching, forests, and outdoor environments."
    )
    local_experiences: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for active, destination-native excursions and workshops (e.g., snorkeling, local horseback riding, cooking classes)."
    )
    personal_privacy: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for quiet, secluded, or low-density destinations away from heavy tourist crowds."
    )
    secluded_remote: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for rural, off-the-grid, or isolated geographic locations."
    )
    culinary: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Importance of exceptional local food scenes, dining options, food tours, markets, and culinary experiences."
    )
    family_friendly: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for safe, kid-friendly environments, easy logistics, and family-oriented amenities."
    )
    walkability_transit: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Preference for highly walkable destinations with reliable public transportation over car rentals."
    )

    def to_vector(self) -> List[float]:
        """Returns deterministic 9-dimensional vector for PyTorch tensor conversion."""
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
            self.walkability_transit
        ]

class UserPreferenceSchema(BaseModel):
    raw_query: str
    max_budget: float | None = None
    duration_days: int = Field(..., gt=0, le=60)
    start_date: date | None = None
    end_date: date | None = None
    weights: PreferenceWeights = Field(default_factory=PreferenceWeights)
