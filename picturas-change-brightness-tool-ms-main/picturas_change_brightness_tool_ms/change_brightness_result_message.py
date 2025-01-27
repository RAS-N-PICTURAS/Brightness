from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .change_brightness_request_message import ChangeBrightnessRequestMessage

"""
response = {
    "messageId": parameters.get("messageId", "unknown"),
    "user_id": parameters.get("user_id", "unknown"),
    "project_id": parameters.get("project_id", "unknown"),
    "status": "error",
    "output": {"type": "image","imageURI": output_uri,}, # OPTIONAL
    "error": {"code": "INVALID_INPUT","message": str(e),"details": {"inputFileURI": parameters.get("inputImageURI", "unknown")}}, # OPTIONAL
    "metadata": {
        "microservice": "ChangeBrightnessTool"
    }
}
"""

class ChangeBrightnessResultOutput(BaseModel):
    """
    Defines the output format for the ChangeBrightness result.
    """
    messageId: str
    user_id: str
    project_id: str
    status: str
    error: dict
    output: dict
    metadata: dict


class ChangeBrightnessResultMessage(ResultMessage[ChangeBrightnessResultOutput]):
    """
    Defines the result message structure for the ChangeBrightness tool.
    """

    def __init__(self, request: ChangeBrightnessRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            # Set output only if no exception occurred
            self.output = ChangeBrightnessResultOutput(
                messageId=tool_result["messageId"],
                user_id=tool_result["user_id"],
                project_id=tool_result["project_id"],
                status=tool_result["status"],
                error=tool_result.get("error", {}),
                output=tool_result.get("output", {}),
                metadata=tool_result["metadata"]
            )
