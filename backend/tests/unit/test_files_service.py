from pathlib import Path

import pytest

from src.files.files_service import FilesService


@pytest.fixture
def subject() -> FilesService:
    return FilesService()


@pytest.fixture
def input_root_data_directory(tmp_path: Path) -> Path:
    root_data_directory = tmp_path / "root"
    root_data_directory.mkdir()
    return root_data_directory


class TestGetAvailableFileNames:
    def test_should_raise_error_when_root_data_directory_is_not_a_directory(
        self, subject: FilesService, tmp_path: Path
    ):
        input_root_data_directory = tmp_path / "not_a_directory"
        input_root_data_directory.write_text("This is a file, not a directory.")
        input_sub_directory = "valid_sub_directory"

        with pytest.raises(ValueError, match="Invalid root data directory"):
            subject.get_available_file_names(input_root_data_directory, input_sub_directory)

    def test_should_raise_error_when_root_data_directory_does_not_exist(self, subject: FilesService, tmp_path: Path):
        input_root_data_directory = tmp_path / "non_existent_directory"
        input_sub_directory = "valid_sub_directory"

        with pytest.raises(ValueError, match="Invalid root data directory"):
            subject.get_available_file_names(input_root_data_directory, input_sub_directory)

    def test_should_raise_error_when_sub_directory_not_in_root_data_directory(
        self, subject: FilesService, input_root_data_directory: Path
    ):
        input_sub_directory = "../outside_root"

        with pytest.raises(ValueError, match=r"Invalid sub-directory: ../outside_root"):
            subject.get_available_file_names(input_root_data_directory, input_sub_directory)

    def test_should_raise_error_when_sub_directory_is_not_a_directory(
        self, subject: FilesService, input_root_data_directory: Path
    ):
        input_sub_directory = "not_a_directory"
        (input_root_data_directory / input_sub_directory).write_text("This is a file, not a directory.")

        with pytest.raises(ValueError, match="Invalid directory: not_a_directory"):
            subject.get_available_file_names(input_root_data_directory, input_sub_directory)

    def test_should_raise_error_when_sub_directory_does_not_exist(
        self, subject: FilesService, input_root_data_directory: Path
    ):
        input_sub_directory = "non_existent_directory"

        with pytest.raises(ValueError, match="Invalid directory: non_existent_directory"):
            subject.get_available_file_names(input_root_data_directory, input_sub_directory)

    def test_should_return_file_names_when_sub_directory_is_valid(
        self, subject: FilesService, input_root_data_directory: Path
    ):
        input_sub_directory = "valid_directory"
        valid_directory_path = input_root_data_directory / input_sub_directory
        valid_directory_path.mkdir()
        (valid_directory_path / "file1.txt").write_text("File 1")
        (valid_directory_path / "file2.txt").write_text("File 2")

        actual = subject.get_available_file_names(input_root_data_directory, input_sub_directory)

        assert set(actual) == {"file1.txt", "file2.txt"}

    def test_should_return_filtered_file_names_when_filter_is_provided(
        self, subject: FilesService, input_root_data_directory: Path
    ):
        input_sub_directory = "valid_directory"
        valid_directory_path = input_root_data_directory / input_sub_directory
        valid_directory_path.mkdir()
        (valid_directory_path / "file.txt").write_text("File 1")
        (valid_directory_path / "other.txt").write_text("File 2")
        (valid_directory_path / "another_file.txt").write_text("Another File")

        actual = subject.get_available_file_names(input_root_data_directory, input_sub_directory, name_filter="file")

        assert set(actual) == {"file.txt", "another_file.txt"}
