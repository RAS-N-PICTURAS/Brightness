from pydantic import BaseModel
from .core.messages.request_message import RequestMessage


class ChangeBrightnessParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    brightnessFactor: float  # Fator de brilho (1.0 = sem alteração, >1.0 = mais brilho, <1.0 = menos brilho)


ChangeBrightnessRequestMessage = RequestMessage[ChangeBrightnessParameters]
