from pathlib import Path

from loguru import logger


class FilesService:
    """Service for handling file operations."""

    def get_available_file_names(
        self, root_data_directory: Path, sub_directory: str, name_filter: str | None = None
    ) -> list[str]:
        """Get the names of available files in the specified sub-directory."""
        if not root_data_directory.is_dir():
            error_log_msg = f"{root_data_directory} is not a valid directory."
            logger.error(error_log_msg)
            public_log_msg = "Invalid root data directory"
            raise ValueError(public_log_msg)

        root_data_directory = root_data_directory.resolve()
        sub_directory_path = (root_data_directory / sub_directory).resolve(strict=False)

        if not sub_directory_path.is_relative_to(root_data_directory):
            error_log_msg = (
                f"{sub_directory_path} is not a valid sub-directory of {root_data_directory}."
                "Access to directories outside the root data directory is not allowed."
                "It can be a potential security risk."
            )
            logger.error(error_log_msg)
            public_log_msg = f"Invalid sub-directory: {sub_directory}"
            raise ValueError(public_log_msg)

        if not sub_directory_path.is_dir():
            error_log_msg = f"{sub_directory_path} is not a valid directory."
            logger.error(error_log_msg)
            public_log_msg = f"Invalid directory: {sub_directory}"
            raise ValueError(public_log_msg)

        file_names = [f.name for f in sub_directory_path.iterdir() if f.is_file()]
        if name_filter:
            file_names = [name for name in file_names if name_filter in name]
        if name_filter is None:
            logger.info(f"Found {len(file_names)} files in {sub_directory}")
        else:
            logger.info(f"Found {len(file_names)} files in {sub_directory} with filter '{name_filter}'")
        return file_names
