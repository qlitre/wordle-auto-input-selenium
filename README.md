# wordle-auto-input-selenium

WordleをSeleniumで自動入力するスクリプトです。

# 動作確認環境

- Windows 10 Home
- Microsoft Edge バージョン 98.0.1108.50 (公式ビルド) (64 ビット)
- Google Chrome バージョン: 98.0.4758.102（Official Build） （64 ビット）

# 動作イメージ

![Animation_5](https://user-images.githubusercontent.com/77523162/153746380-55aa0257-ee55-4748-aee1-bb0274ec0dc2.gif)

# つかいかた

まずはお使いのブラウザのバージョンに合わせて、web driverを入手してください。

Edge
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

Chrome
https://chromedriver.chromium.org/downloads

環境に合わせて`settings.py`内のPathを編集してください。

```
"""変数を定義"""

from pathlib import Path

...
EDGE_DRIVER = f'{BASE_DIR}\edgedriver_win64\msedgedriver.exe'
CHROME_DRIVER = f'{BASE_DIR}\chromedriver_win32\chromedriver.exe'
...

```

つぎに`wordle_auto_solver.py`を開いてブラウザと一番最初に打つ単語を入力してください。

```
from chrome import chrome_browser
from edge import edge_browser

...

if __name__ == '__main__':
    # ブラウザを指定
    _browser = chrome_browser()
    # 最初の単語
    first = 'puppy'
    job(browser=_browser, first_input=first)

```

あとは`wordle_auto_solver.py`を起動させると、自動入力が始まります。
