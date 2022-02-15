"""変数を定義"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EDGE_DRIVER = f'{BASE_DIR}\edgedriver_win64\msedgedriver.exe'
CHROME_DRIVER = f'{BASE_DIR}\chromedriver_win32\chromedriver.exe'
WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'
WORDLE_ANSWER_TEXT = f'{BASE_DIR}\wordle.txt'
