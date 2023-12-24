from pathlib import Path
from typing import Union

DEFAULT_WAIT_TIME: int = 2
PAGE_LOAD_TIME: int = 15
URLS_LIMIT: Union[int, None] = 3

ROOT_DIR = Path(__file__).parent.parent.resolve()
urls_path = ROOT_DIR / "files/urls.txt"
htmls_dir = ROOT_DIR / "files/html_files"
texts_dir = ROOT_DIR / "files/txt_files"

# TODO: Make this dynamic
right_click_pst = {"x": 984, "y": 204}
