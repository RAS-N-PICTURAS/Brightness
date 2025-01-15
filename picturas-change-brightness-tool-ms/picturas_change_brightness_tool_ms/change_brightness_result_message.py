from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .change_brightness_request_message import ChangeBrightnessRequestMessage


class ChangeBrightnessResultOutput(BaseModel):
    """
    Defines the output format for the ChangeBrightness result.
    """
    type: str
    imageURI: str


class ChangeBrightnessResultMessage(ResultMessage[ChangeBrightnessResultOutput]):
    """
    Defines the result message structure for the ChangeBrightness tool.
    """

    def __init__(self, request: ChangeBrightnessRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            # Set output only if no exception occurred
            self.output = ChangeBrightnessResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
