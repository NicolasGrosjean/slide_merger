import requests
from loguru import logger

from src.utils import manage_request_error


class SlideMerger:
    """Class to handle merge of slides."""

    def __init__(self, slide_merge_url: str, timeout: int):
        self.slide_merge_url = slide_merge_url
        self.timeout = timeout

    def merge_slides(self, input_slides: list[str], output_file_name: str) -> None:
        """Merge slides from the input PowerPoint presentations into a single presentation."""
        logger.info(f"Merging {len(input_slides)} slides into {output_file_name}")
        request_data = {
            "input_slides": input_slides,
            "output_file_name": output_file_name,
        }
        response = requests.post(self.slide_merge_url, json=request_data, timeout=self.timeout)
        manage_request_error(response)
        logger.info(f"Slides merged successfully into {output_file_name}")
