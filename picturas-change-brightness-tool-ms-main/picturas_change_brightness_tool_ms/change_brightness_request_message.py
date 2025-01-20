from pydantic import BaseModel
from .core.messages.request_message import RequestMessage


class ChangeBrightnessParameters(BaseModel):
    messageId: str
    user_id: str
    project_id: str
    inputImageURI: str
    configValue: float  # Fator de brilho (1.0 = sem alteração, >1.0 = mais brilho, <1.0 = menos brilho)
    configColor: str # Not used in this tool


ChangeBrightnessRequestMessage = RequestMessage[ChangeBrightnessParameters]
