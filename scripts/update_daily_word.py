import pandas as pd
import random
from datetime import datetime
import os
import sys
import re 

def get_daily_seed():
    """
    今日の日付からシード値を生成します。
    毎日同じ言葉が選ばれるように、日付に基づいたシードを使用します。
    """
    today = datetime.now()
    return today.year * 10000 + today.month * 100 + today.day

def get_todays_word(csv_file='data/words.csv'):
    """
    CSVファイルから今日の言葉をランダムに1つ取得します。
    """
    try:
        # CSVファイルを読み込みます
        df = pd.read_csv(csv_file, encoding='utf-8')

        # 必要な列が全て存在するか確認します
        required_columns = ['言葉', '話されている国（国旗）', '日本語読み', '日本語の意味']
        if not all(col in df.columns for col in required_columns):
            print(f"エラー: CSVファイルに必要な列がありません: {required_columns}")
            return None

        # 空の行を除去します
        df = df.dropna()

        if len(df) == 0:
            print("エラー: 有効なデータがありません。CSVファイルに言葉を追加してください。")
            return None

        # 今日の日付をシードとして使用し、ランダム選択の再現性を保証します
        seed = get_daily_seed()
        random.seed(seed)

        # データフレームからランダムに1行を選択します
        selected_word = df.sample(n=1).iloc[0]

        return {
            'word': selected_word['言葉'],
            'country': selected_word['話されている国（国旗）'],
            'pronunciation': selected_word['日本語読み'],
            'meaning': selected_word['日本語の意味']
        }

    except FileNotFoundError:
        print(f"エラー: CSVファイルが見つかりません: {csv_file}")
        return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def create_daily_word_section_markdown(word_data):
    """
    「今日の言葉」セクションのMarkdownコンテンツのみを生成します。
    README.mdの他の部分は含みません。
    """
    today = datetime.now().strftime('%Y年%m月%d日')
    weekday = datetime.now().strftime('%A')
    weekday_jp = {
        'Monday': '月曜日',
        'Tuesday': '火曜日',
        'Wednesday': '水曜日',
        'Thursday': '木曜日',
        'Friday': '金曜日',
        'Saturday': '土曜日',
        'Sunday': '日曜日'
    }.get(weekday, weekday)

    if not word_data:
        word_content = f"""
## 🌟 今日の言葉

**エラー**: 今日の言葉を取得できませんでした。`data/words.csv` ファイルを確認してください。
"""
    else:
        word_content = f"""
## 🌟 今日の言葉

**{today} ({weekday_jp})**

<div align="center">

### {word_data['word']}

**{word_data['country']}**

*{word_data['pronunciation']}*

**「{word_data['meaning']}」**

</div>

---
"""
    return word_content.strip() # 生成されたMarkdownの余分な空白を除去

def update_readme():
    """
    README.mdの指定されたセクション（今日の言葉）のみを更新します。
    """
    readme_file = 'README.md'
    start_marker = "<!-- START_SECTION:daily-word -->"
    end_marker = "<!-- END_SECTION:daily-word -->"

    # 今日の言葉のデータを取得します
    word_data = get_todays_word()

    # 「今日の言葉」セクションの新しいMarkdownコンテンツを生成します
    new_daily_word_section = create_daily_word_section_markdown(word_data)

    try:
        # 既存のREADME.mdの内容を読み込みます
        with open(readme_file, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        # マーカー間の内容を置換するための正規表現を作成します
        # re.escape()を使って、マーカー文字列内の特殊文字をエスケープします
        # (.*?)は非貪欲マッチで、マーカー間の任意の文字（改行を含む）にマッチします
        # re.DOTALLフラグは、.が改行にもマッチするようにします
        pattern = re.compile(
            re.escape(start_marker) + r"(.*?)" + re.escape(end_marker),
            re.DOTALL
        )

        # 正規表現にマッチする部分（マーカーとその間のコンテンツ）を置換します
        # 新しいコンテンツは、開始マーカー、新しいセクション、終了マーカーの順に挿入されます
        updated_readme_content = pattern.sub(
            f"{start_marker}\n{new_daily_word_section}\n{end_marker}",
            readme_content,
            count=1 # 最初に見つかった1箇所のみ置換
        )

        # 更新された内容をREADME.mdファイルに書き込みます
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(updated_readme_content)
        print("README.md の「今日の言葉」セクションを正常に更新しました。")

        if word_data:
            print(f"今日の言葉: {word_data['word']} ({word_data['meaning']})")

    except FileNotFoundError:
        print(f"エラー: README.md ファイルが見つかりません: {readme_file}")
    except Exception as e:
        print(f"README.md の更新中にエラーが発生しました: {e}")

if __name__ == "__main__":
    update_readme()
