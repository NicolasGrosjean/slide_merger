from pathlib import Path

from fastapi.testclient import TestClient
from httpx2 import Response
from pytest_mock import MockerFixture

from src.webapi.settings import Settings


class TestMergeSlides:
    def test_should_return_the_created_presentation(
        self, settings: Settings, client: TestClient, mocker: MockerFixture
    ):
        output_file_name = "merged.pptx"
        output_content = b"merged presentation"

        def create_output_file(_self: object, _input_slides: list[Path], output_path: Path) -> None:
            output_path.write_bytes(output_content)

        mocker.patch("src.slide_merger.slide_merger_service.SlideMergerService.merge", create_output_file)

        response: Response = client.post(
            "/slide_merger/merge",
            json={"input_slides": ["input.pptx"], "output_file_name": output_file_name},
        )

        assert response.status_code == 200
        assert response.content == output_content
        assert response.headers["content-type"] == (
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        assert response.headers["content-disposition"] == f'attachment; filename="{output_file_name}"'
        assert (settings.root_data_directory / output_file_name).read_bytes() == output_content


class TestAvailableFileNames:
    def test_should_raise_error_when_sub_directory_not_in_root_data_directory(self, client: TestClient):
        input_sub_directory = "../outside_root"

        response: Response = client.get("/files/filenames", params={"sub_directory": input_sub_directory})
        assert response.status_code == 500
        assert response.json() == {"detail": "Invalid sub-directory: ../outside_root"}

    def test_should_return_filtered_file_names_when_filter_is_provided(self, settings: Settings, client: TestClient):
        input_sub_directory = "valid_directory"
        valid_directory_path = settings.root_data_directory / input_sub_directory
        valid_directory_path.mkdir()
        (valid_directory_path / "file.txt").write_text("File 1")
        (valid_directory_path / "other.txt").write_text("File 2")
        (valid_directory_path / "another_file.txt").write_text("Another File")

        response: Response = client.get(
            "/files/filenames", params={"sub_directory": input_sub_directory, "name_filter": "file"}
        )
        assert response.status_code == 200
        actual = response.json()
        assert set(actual) == {"file.txt", "another_file.txt"}
