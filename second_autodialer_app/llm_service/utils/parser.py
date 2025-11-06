from pydantic import BaseModel, validator, Field
import re, json

class CommandSchema(BaseModel):
    action: str | None = Field(default=None, description="Action to perform, e.g., 'call'")
    number: str | None = Field(default=None, description="Phone number to call")
    command: str | None = Field(default=None, description="User message or instruction")

    @validator("number", pre=True, always=True)
    def validate_number(cls, value):
        if not value:
            return None
        cleaned = re.sub(r"[^\d+]", "", str(value))
        if not re.fullmatch(r"\+?\d{10,15}", cleaned):
            return None
        return cleaned

def parse_ai_response(raw_response: str) -> dict:
    try:
        json_match = re.search(r"\{[\s\S]*\}", raw_response)
        if json_match:
            json_str = json_match.group(0)
            data = json.loads(json_str)
            validated = CommandSchema(**data)
            return validated.dict()
    except Exception as e:
        print(f"[parse_ai_response] JSON parsing failed: {e}")

    num_match = re.search(r"\+?\d[\d\s\-]{8,16}\d", raw_response)
    number = None
    if num_match:
        number = re.sub(r"[^\d+]", "", num_match.group())

    return CommandSchema(
        action="call" if "call" in raw_response.lower() else None,
        number=number,
        command=None
    ).dict()
