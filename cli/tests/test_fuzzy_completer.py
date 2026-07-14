from prompt_toolkit.document import Document

from src.fuzzy_completer import FuzzyCompleter
from tests.conftest import generate_random_str


def test_fuzzy_completer_returns_fuzzy_matches() -> None:
    completer = FuzzyCompleter(["apple", "banana", "apricot"], max_value_nb=5)
    document = Document(text="app")

    completions = list(completer.get_completions(document, complete_event=None))

    assert {completion.text for completion in completions} == {"apple", "apricot", "banana"}


def test_fuzzy_completer_respects_limit() -> None:
    completer = FuzzyCompleter(["apple", generate_random_str(), generate_random_str()], max_value_nb=1)
    document = Document(text="appel")

    completions = list(completer.get_completions(document, complete_event=None))

    assert {completion.text for completion in completions} == {"apple"}
