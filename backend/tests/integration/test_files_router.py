from fastapi.testclient import TestClient
from httpx import Response

from src.webapi.settings import Settings


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
