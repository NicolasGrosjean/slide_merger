import argparse

from loguru import logger

from src.file_selector import FileSelector
from src.settings import Settings
from src.slide_merger import SlideMerger
from src.utils import set_log_level


def main(output_path: str) -> None:
    """Select files and merge them according settings."""
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
    logger.debug(f"Selected files: {slides}")
    sm = SlideMerger(
        slide_merge_url=settings.api_client.slide_merge_url, timeout=settings.api_client.slide_merge_timeout
    )
    sm.merge_slides(input_slides=slides, output_file_name=output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool to merge slides from multiple PowerPoint presentations into a single presentation."
    )
    parser.add_argument("output_path", type=str, help="Path to the output merged presentation.")
    args = parser.parse_args()
    main(args.output_path)
