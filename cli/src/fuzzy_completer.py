from typing import TYPE_CHECKING

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from rapidfuzz import process

if TYPE_CHECKING:
    from collections.abc import Iterable

    from prompt_toolkit.completion import CompleteEvent
    from prompt_toolkit.document import Document


class FuzzyCompleter(Completer):
    """A completer that uses fuzzy matching to provide suggestions based on a list of values."""

    def __init__(self, values: list[str], max_value_nb: int):
        self.__values = values
        self.__max_value_nb = max_value_nb

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        """Get completions for the given document based on fuzzy matching."""
        query = document.text
        matches = process.extract(query, self.__values, limit=self.__max_value_nb)

        for match, _, _ in matches:
            yield Completion(match, start_position=-len(query))
