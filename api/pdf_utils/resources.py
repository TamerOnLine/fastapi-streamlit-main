"""
Utilities for extracting embedded package resources into temporary files.
Useful for runtime access to bundled assets.
"""

from importlib import resources
from pathlib import Path
import tempfile
import shutil


def extract_resource(package: str, resource: str) -> Path:
    """
    Copies a package-embedded resource to a temporary file and returns its path.

    Example:
        extract_resource("pdf_utils.assets", "NotoNaskhArabic-Regular.ttf")

    Args:
        package (str): The name of the package containing the resource.
        resource (str): The name of the resource file to extract.

    Returns:
        Path: Path to the extracted temporary file.
    """
    with resources.files(package).joinpath(resource).open("rb") as src:
        tmpdir = Path(tempfile.mkdtemp(prefix="pdf_assets_"))
        out = tmpdir / Path(resource).name
        with out.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        return out