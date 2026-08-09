import pytest
import requests
import responses

from src.slide_merger import SlideMerger


@responses.activate
def test_get_file_names_success() -> None:
    mock = responses.post("http://example", status=200)
    fs = SlideMerger("http://example", timeout=1)
    fs.merge_slides(["sub/one.txt", "sub/two.txt"], "output.pptx")
    assert mock.call_count == 1


@responses.activate
def test_get_file_names_error_returns_empty() -> None:
    mock = responses.post("http://example", status=500)
    fs = SlideMerger("http://example", timeout=1)
    with pytest.raises(requests.exceptions.HTTPError):
        fs.merge_slides(["sub/one.txt", "sub/two.txt"], "output.pptx")
    assert mock.call_count == 1
