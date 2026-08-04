import requests
from loguru import logger
from prompt_toolkit import PromptSession

from src.fuzzy_completer import FuzzyCompleter
from src.settings import SlidePartSettings
from src.utils import manage_request_error


class FileSelector:
    """Class to handle file selection from a sub-directory with optional name filtering."""

    def __init__(self, filenames_url: str, timeout: int):
        self.filenames_url = filenames_url
        self.timeout = timeout

    def interactive_select_file(self, slide_part_settings: SlidePartSettings, max_file_suggestion_nb: int) -> str:
        """Interactively select a file name from the given sub-directory with name filtering."""
        files = self._get_file_names(slide_part_settings.subdirectory, slide_part_settings.name_filter)
        if slide_part_settings.placeholder:
            files.append(slide_part_settings.placeholder)
        completer = FuzzyCompleter(files, max_value_nb=max_file_suggestion_nb)
        session: PromptSession = PromptSession(completer=completer)

        description = slide_part_settings.description or "Select a file"
        query = " (start to type, select with arrow and press Enter to select): "
        res = session.prompt(description + query)
        if res not in files:
            logger.warning(f"Selected file '{res}' is not in the available files list. Using placeholder instead.")
            res = slide_part_settings.placeholder
        return f"{slide_part_settings.subdirectory}/{res}"

    def _get_file_names(self, sub_directory: str, name_filter: str | None) -> list[str]:
        r = requests.get(
            self.filenames_url,
            params={
                "sub_directory": sub_directory,
                "name_filter": name_filter,
            },
            timeout=self.timeout,
        )
        manage_request_error(r)
        return r.json()
