# wordle-auto-input-selenium
WordleをSeleniumで自動入力するスクリプトです。

# 動作確認環境
- Windows 10 Home
- Microsoft Edge バージョン 98.0.1108.50 (公式ビルド) (64 ビット)

# 動作イメージ
![Animation_5](https://user-images.githubusercontent.com/77523162/153746380-55aa0257-ee55-4748-aee1-bb0274ec0dc2.gif)

# つかいかた

まずはお使いのEdgeのバージョンに合わせて、web driverを入手してください。

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

環境に合わせて`settings.py`内のEDGE_DRIVERを編集してください。

```
"""
変数を定義するだけのファイル
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EDGE_DRIVER = f'{BASE_DIR}\edgedriver_win64\msedgedriver.exe'
WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'
WORDLE_ANSWER_TEXT = f'{BASE_DIR}/wordle.txt'
```

つぎに`wordle_auto_solver.py`を開いて一番最初に打つ単語を入力してください。

```
...

if __name__ == '__main__':
    first = 'mamma'
    job(first)
```

あとは`wordle_auto_solver.py`を起動させると、自動入力が始まります。
