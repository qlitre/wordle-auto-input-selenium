"""
Wordleをseleniumで自動入力するファイル
"""

from settings import WORDLE_URL, WORDLE_ANSWER_TEXT
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from chrome import chrome_browser
from edge import edge_browser
import time
import pandas as pd
import sys


class WordListEmptyError(Exception):
    """入力単語候補がなくなったことを知らせる例外クラス"""
    pass


def generate_df_row():
    """dfのrowをyieldして返す"""
    with open(WORDLE_ANSWER_TEXT, "r") as f:
        for word in f:
            word = word.strip()
            yield [word[0], word[1], word[2], word[3], word[4], word]


def create_df():
    """dfを作成"""
    cols = ['char_1', 'char_2', 'char_3', 'char_4', 'char_5', 'char_full']
    values = [row for row in generate_df_row()]
    return pd.DataFrame(values, columns=cols)


def filter_correct(df, col_name, char):
    """緑ヒントの時のフィルタ"""
    return df[df[col_name].str.contains(char)]


def filter_present(df, col_name, char):
    """黄色ヒントの時のフィルタ"""
    df = df[~df[col_name].str.contains(char)]
    return df[df['char_full'].str.contains(char)]


def filter_absent(df, char):
    """灰色ヒントの時のフィルタ"""
    return df[~df['char_full'].str.contains(char)]


def guess_word(df):
    """
    dfから単語を返す
    todo ここで一番答えに近づく単語を返したい
    """
    word = df['char_full'].values[0]
    return word


def open_wordle(browser):
    """wordleページを開く処理"""
    browser.get(WORDLE_URL)
    # ここでモーダルが出現するのでちょっと待つ
    time.sleep(.5)
    # 一回クリックしてモーダルを消す
    elm = browser.find_element(By.CSS_SELECTOR, "body")
    elm.click()
    time.sleep(.5)


def find_game_rows(browser):
    """game row elementsを返す"""
    host = browser.find_element(By.TAG_NAME, "game-app")
    board = browser.execute_script("return arguments[0].shadowRoot.getElementById('board')", host)
    return board.find_elements(By.TAG_NAME, 'game-row')


def find_game_tiles(browser, game_row):
    """タイル（文字入力マス）を返す"""
    row = browser.execute_script("return arguments[0].shadowRoot.querySelector('.row')", game_row)
    return row.find_elements(By.TAG_NAME, 'game-tile')


def input_word(browser, word):
    """Wordleサイトに単語を打ちこんでEnterキーを押す処理"""
    elm = browser.find_element(By.CSS_SELECTOR, "body")
    for char in word:
        elm.send_keys(char)
    time.sleep(1)
    elm.send_keys(Keys.ENTER)
    # パネルがひっくり返ってヒントが表示されている時間、長めに待つ
    time.sleep(2)


def stop_selenium(msg):
    """
    seleniumが終了するとブラウザが閉じるので、inputで保持
    todo たぶんもっと良い方法があると思う
    """
    print(msg)
    input('終了するには何かキーを押してください')
    sys.exit()


class Results:
    """
    例えば
    answer:ULTRA
    guess :MAMMA
    という場合に2番目のAは灰色(absent)、5番目のAは(correct)となる。
    この状態で単語リストをフィルターをすると推測リストが空になる。
    これを防ぐために、結果を整理して返すためのクラス
    つまり、この場合、2番目の灰色は除外する
    """

    def __init__(self):
        self.results = []

    def add_result(self, col_name, char, hint):
        """結果を加える"""
        self.results.append({'col_name': col_name,
                             'char': char,
                             'hint': hint})

    def is_char_has_other_hint(self, char, hint):
        """文字が他のヒントを持っていないか調べる"""
        _results = self.results
        _results = list(filter(lambda x: x['char'] == char, _results))
        _results = list(filter(lambda x: x['hint'] != hint, _results))
        if _results:
            return True
        else:
            return False

    def get_result(self):
        """結果を返す"""
        for result in self.results:
            col_name = result['col_name']
            char = result['char']
            hint = result['hint']
            # absentの時にその文字が他のヒントで使われていたらスキップ
            if hint == 'absent':
                if self.is_char_has_other_hint(char, hint):
                    continue
            yield col_name, char, hint


def job(browser, first_input):
    """メインジョブ"""

    # 単語リストデータ
    df = create_df()

    # wordleページを開く
    open_wordle(browser)

    # game rowsを取得
    # wordleの入力ボックスの部分、6行分がリストで取得される
    game_rows = find_game_rows(browser)

    for turn, game_row in enumerate(game_rows, 1):

        # 単語を画面に入力する
        if turn == 1:
            input_word(browser, first_input)

        # 2ターン目以降はdfから単語を取得
        else:
            if len(df) == 0:
                raise WordListEmptyError(f'単語リストがなくなりました。恐らく答えが{WORDLE_ANSWER_TEXT}にないです。')
            word = guess_word(df)
            input_word(browser, word)

        # tileを取得。文字を打ち込むマス。５マス文がリストで返る
        game_tiles = find_game_tiles(browser, game_row)

        # クリア判定で使用
        clear_flag = True

        # 結果整理クラス
        results = Results()

        # 1マスずつ繰り返して結果を保存していく
        for col_num, game_tile in enumerate(game_tiles, 1):
            tile = browser.execute_script("return arguments[0].shadowRoot.querySelector('.tile')", game_tile)
            col_name = f'char_{col_num}'
            char = tile.text.lower()

            # 緑がcorrect,黄色がpresent,灰色がabsentで返る
            hint = tile.get_attribute("data-state")
            results.add_result(col_name, char, hint)

            # correctじゃないのが一つでもあったらクリアではない
            if hint != 'correct':
                clear_flag = False

        if clear_flag:
            stop_selenium('GameClear')

        # 6ターン目でここまで来ていたらゲーム失敗
        if turn == 6:
            stop_selenium('GameOver')

        # 答えを次に向けて絞り込む
        for col_name, char, hint in results.get_result():
            if hint == 'correct':
                df = filter_correct(df, col_name, char)
            if hint == 'present':
                df = filter_present(df, col_name, char)
            if hint == 'absent':
                df = filter_absent(df, char)


if __name__ == '__main__':
    # ブラウザを指定
    _browser = chrome_browser()
    first = 'puppy'
    job(browser=_browser, first_input=first)
