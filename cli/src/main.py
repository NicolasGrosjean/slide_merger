# ruff: noqa
import os

from prompt_toolkit import PromptSession

from src.fuzzy_completer import FuzzyCompleter


def _interactive_select_file(directory: str) -> str:
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    completer = FuzzyCompleter(files, max_value_nb=2)
    session: PromptSession = PromptSession(completer=completer)

    print(f"\nSelect a file from {directory}")
    result = session.prompt("Query: ")
    return result


directories = [
    "../data/placeholder",
]


final_choices = []
for d in directories:
    choice = _interactive_select_file(d)
    final_choices.append(choice)

print("\nFinal selections:")
for c in final_choices:
    print(c)
