import os


def test_data_path(file_path):
    """Return the path of file in the directory with the test data."""
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_data/',
        file_path
    )

    return path
