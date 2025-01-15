from PIL import Image, ImageEnhance
from .core.tool import Tool
from .change_brightness_request_message import ChangeBrightnessParameters


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
        # Abrir a imagem de entrada
        try:
            with Image.open(parameters.inputImageURI) as img:
                # Ajustar o brilho com o fator fornecido
                enhancer = ImageEnhance.Brightness(img)
                adjusted_image = enhancer.enhance(parameters.brightnessFactor)
                
                # Salvar a imagem ajustada
                adjusted_image.save(parameters.outputImageURI)
                
            return f"Brightness adjusted with factor {parameters.brightnessFactor} and saved to {parameters.outputImageURI}"
        
        except FileNotFoundError:
            raise Exception(f"Input image not found at {parameters.inputImageURI}")
        except Exception as e:
            raise Exception(f"An error occurred while processing the image: {str(e)}")
