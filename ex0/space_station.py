from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: str | None = Field(None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 42)
    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=13.5,
            oxygen_level=56.7,
            last_maintenance="2024-02-29"
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    print(f"Status: {("Operational" if valid_station.is_operational
                      is True else "Not Operational")}\n")
    print("=" * 42)

    try:
        invalid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=23,
            power_level=13.5,
            oxygen_level=56.7,
            last_maintenance="2024-01-15T10:30:00",
            is_operational=False
        )
        print(invalid_station)
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return


if __name__ == "__main__":
    main()
