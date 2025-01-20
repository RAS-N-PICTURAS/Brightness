import json
import random
import string
from PIL import Image, ImageEnhance
from .core.tool import Tool
from .change_brightness_request_message import ChangeBrightnessParameters
from .image_uri_utils import data_uri_to_image_file, image_to_data_uri

class ChangeBrightnessTool(Tool):
    """
    Tool to adjust the brightness of an image.
    """

    def apply(self, parameters: ChangeBrightnessParameters) -> str:
        """
        Apply brightness adjustment to the input image and save the result.

        Args:
            parameters (ChangeBrightnessParameters): Parameters including input image URI,
                                                     output image URI, and brightness factor.

        Returns:
            str: A message indicating success and the output path.
        """
        try:
            # Extract input parameters
            user_id = parameters["user_id"]
            project_id = parameters["project_id"]
            input_image_uri = parameters["inputImageURI"]
            brightness_factor = float(parameters["configValue"])
            
            # Convert input URI to PIL image
            img = data_uri_to_image_file(input_image_uri)
            
            image = Image.open(img)
            
            # Adjust brightness
            enhancer = ImageEnhance.Brightness(image)
            adjusted_image = enhancer.enhance(brightness_factor)
            
            # Save the adjusted image to a temporary file
            temp_output_path = "/tmp/adjusted_image.png"
            adjusted_image.save(temp_output_path)
            
            tmp_image = Image.open(temp_output_path)
            
            # Convert the output file to URI
            output_uri = image_to_data_uri(tmp_image)
            
            # Build success response
            response = {
                "messageId": ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)),
                "user_id": user_id,
                "project_id": project_id,
                "status": "success",
                "error": {},
                "output": {
                    "type": "image",
                    "imageURI": output_uri,
                },
                "metadata": {
                    "microservice": "ChangeBrightnessTool"
                }
            }
            
        except Exception as e:
            # Build error response
            response = {
                "messageId": ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)),
                "user_id": parameters.get("user_id", "unknown"),
                "project_id": parameters.get("project_id", "unknown"),
                "status": "error",
                "error": {
                    "code": "INVALID_INPUT",
                    "message": str(e),
                    "details": {
                        "inputFileURI": parameters.get("inputImageURI", "unknown")
                    }
                },
                "output": {},
                "metadata": {
                    "microservice": "ChangeBrightnessTool"
                }
            }
        
        # Return the response as a JSON string
        return json.dumps(response)
