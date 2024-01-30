from pathlib import Path


def test_data_path(file_path) -> str:
    """Return the path of file in the directory with the test data."""
    path = Path("/test_data").joinpath(file_path)
    return str(path)
