import pytest
import responses
from pytest_mock import MockerFixture

from src.file_selector import FileSelector
from src.settings import SlidePartSettings


class FakeSession:
    def __init__(self, completer=None, return_value=""):
        self._return = return_value

    def prompt(self, *args, **kwargs):
        return self._return


def fake_prompt_session_factory(completer=None):
    return FakeSession(return_value="toto.txt")


@responses.activate
def test_get_file_names_success() -> None:
    mock = responses.get("http://example", json=["one.txt", "two.txt"], status=200)
    fs = FileSelector("http://example", timeout=1)
    names = fs._get_file_names("sub", None)
    assert mock.call_count == 1
    assert names == ["one.txt", "two.txt"]


@responses.activate
def test_get_file_names_error_returns_empty() -> None:
    mock = responses.get("http://example", status=500)
    fs = FileSelector("http://example", timeout=1)
    names = fs._get_file_names("sub", None)
    assert mock.call_count == 1
    assert names == []


def test_interactive_select_file_returns_selected(mocker: MockerFixture) -> None:
    mocker.patch.object(FileSelector, "_get_file_names", return_value=["a.txt", "toto.txt"])

    mocker.patch("src.file_selector.PromptSession", fake_prompt_session_factory)

    settings = SlidePartSettings(subdirectory="sub", placeholder="placeholder.txt")
    fs = FileSelector("http://example", timeout=1)

    res = fs.interactive_select_file(settings, max_file_suggestion_nb=5)

    assert res == "sub/toto.txt"


def test_interactive_select_file_not_in_list_uses_placeholder(mocker: MockerFixture) -> None:
    mocker.patch.object(FileSelector, "_get_file_names", return_value=["a.txt", "b.txt"])

    def fake_prompt_session_factory(completer=None):
        return FakeSession(return_value="unknown.txt")

    mocker.patch("src.file_selector.PromptSession", fake_prompt_session_factory)

    settings = SlidePartSettings(subdirectory="sub", placeholder="placeholder.txt")
    fs = FileSelector("http://example", timeout=1)

    res = fs.interactive_select_file(settings, max_file_suggestion_nb=5)

    assert res == "placeholder.txt"


def test_interactive_select_file_missing_placeholder_raises(mocker: MockerFixture) -> None:
    mocker.patch.object(FileSelector, "_get_file_names", return_value=["a.txt"])

    mocker.patch("src.file_selector.PromptSession", fake_prompt_session_factory)

    settings = SlidePartSettings(subdirectory="sub", file_name="some.txt")
    fs = FileSelector("http://example", timeout=1)

    with pytest.raises(ValueError, match="No placeholder provided for the selected slide part"):
        fs.interactive_select_file(settings, max_file_suggestion_nb=5)
