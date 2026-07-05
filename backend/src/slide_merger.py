import contextlib
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger
from pptx_merger import Merger

if TYPE_CHECKING:
    from pathlib import Path


class SlideMerger:
    """Merge slides from multiple PowerPoint presentations into a single presentation."""

    def __init__(self):
        self.__merger = Merger()

    def merge(self, input_slides: list[Path], output_path: Path) -> None:
        """Merge slides from the input PowerPoint presentations into a single presentation."""
        src_docs: list[BytesIO] = []
        merged = None
        try:
            src_docs = [BytesIO(slide.read_bytes()) for slide in input_slides]
            logger.info(f"Merging {len(input_slides)} slides into {output_path}")
            merged = self.__merger.merge_slides(src_docs)
            with output_path.open("wb") as f:
                f.write(merged.getvalue())
                logger.info(f"Merged {len(input_slides)} slides into {output_path}")
        finally:
            for s in src_docs:
                with contextlib.suppress(Exception):
                    s.close()
            if merged:
                with contextlib.suppress(Exception):
                    merged.close()
