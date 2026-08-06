from loguru import logger

from src.file_selector import FileSelector
from src.settings import Settings
from src.utils import set_log_level

settings = Settings()
set_log_level(settings.log_level)
logger.debug(settings)  # TODO Improve with tabulate but make tabulate optional

fs = FileSelector(filenames_url=settings.api_client.filenames_url, timeout=settings.api_client.filename_timeout)
slides: list[str] = []
for slide_part in settings.slides:
    if slide_part.file_name:
        logger.debug(f"Using provided file name: {slide_part.file_name}")
        slides.append(f"{slide_part.subdirectory}/{slide_part.file_name}")
    else:
        res = fs.interactive_select_file(
            slide_part_settings=slide_part, max_file_suggestion_nb=settings.max_file_suggestion_nb
        )
        logger.debug(f"Selected file: {res}")
        slides.append(res)
logger.info(f"Selected files: {slides}")
# TODO Merge slides
