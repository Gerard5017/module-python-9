from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_commander = any(
            m.rank in (Rank.captain, Rank.commander)
            for m in self.crew
        )
        if not has_commander:
            raise ValueError("Mission must have at least one "
                             "Commander or Captain")

        if self.duration_days > 365:
            experimented = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experimented += 1
            if (experimented / len(self.crew) * 100) < 50:
                raise ValueError("Long missions (> 365 days) need 50%"
                                 "experienced crew (5+ years)")

        all_active = all(member.is_active for member in self.crew)
        if not all_active:
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 42)
    try:
        sarah = CrewMember(
            member_id="S001",
            name="Sarah Connor",
            rank=Rank.commander,
            age=27,
            specialization="Mission Command",
            years_experience=9
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return

    try:
        john = CrewMember(
            member_id="J001",
            name="John Smith",
            rank=Rank.lieutenant,
            age=25,
            specialization="Navigation",
            years_experience=7
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return

    try:
        alice = CrewMember(
            member_id="A001",
            name="Alice Johnson",
            rank=Rank.officer,
            age=21,
            specialization="Engineering",
            years_experience=3
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-01-01",
            duration_days=900,
            crew=[sarah, john, alice],
            budget_millions=2500.0
            )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return

    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print("Crew members:")
    for member in valid_mission.crew:
        print(f"- {member.name} ({member.rank.value}) "
              f"- {member.specialization}")
    print()

    print("=" * 42)
    try:
        invalid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-01-01",
            duration_days=900,
            crew=[john, alice],
            budget_millions=2500.0
            )
        print(invalid_mission)
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return


if __name__ == "__main__":
    main()
