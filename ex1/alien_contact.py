from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with AC")

        if (self.contact_type is ContactType.physical
           and self.is_verified is False):
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type is ContactType.telepathic
           and self.witness_count < 3):
            raise ValueError("Telepathic contact requires"
                             " at least 3 witnesses")

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should "
                             "include received messages")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 42)
    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.radio,
            timestamp="2024-12-12",
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
            )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return
    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type.value}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: '{valid_contact.message_received}'")

    print("=" * 42)
    try:
        invalid_contact = AlienContact(
            contact_id="AC2024_001",
            contact_type=ContactType.telepathic,
            timestamp="2024-12-12",
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'])
        return
    print("Valid contact report:")
    print(f"ID: {invalid_contact.contact_id}")
    print(f"Type: {invalid_contact.contact_type.value}")
    print(f"Location: {invalid_contact.location}")
    print(f"Signal: {invalid_contact.signal_strength}/10")
    print(f"Duration: {invalid_contact.duration_minutes} minutes")
    print(f"Witnesses: {invalid_contact.witness_count}")
    print(f"Message: '{invalid_contact.message_received}'")


if __name__ == "__main__":
    main()
