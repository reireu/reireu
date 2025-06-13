import pandas as pd
import random
from datetime import datetime
import os
import sys

def get_daily_seed():
    """今日の日付からシード値を生成"""
    today = datetime.now()
    return today.year * 10000 + today.month * 100 + today.day

def get_todays_word(csv_file='data/words.csv'):
    """CSVファイルから今日の言葉を取得"""
    try:
        # CSVファイルを読み込み
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        # 必要な列があるかチェック
        required_columns = ['言葉', '話されている国（国旗）', '日本語読み', '日本語の意味']
        if not all(col in df.columns for col in required_columns):
            print(f"エラー: CSVファイルに必要な列がありません: {required_columns}")
            return None
            
        # 空の行を除去
        df = df.dropna()
        
        if len(df) == 0:
            print("エラー: 有効なデータがありません")
            return None
            
        # 今日の日付をシードとして使用（毎日同じ結果を保証）
        seed = get_daily_seed()
        random.seed(seed)
        
        # ランダムに1つ選択
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

def create_readme_content(word_data):
    """README.mdの内容を生成"""
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
        word_content = """
## 🌟 今日の言葉

**エラー**: 今日の言葉を取得できませんでした。data/words.csv ファイルを確認してください。
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
    
    readme_content = f"""# 📚 今日の言葉 - Daily Word

毎日新しい言葉を学びましょう！世界中の様々な言語から、その日の特別な言葉をお届けします。

{word_content}

## 📝 使い方

1. `data/words.csv` ファイルに学習したい言葉を追加してください
2. GitHub Actionsが毎日自動的にREADME.mdを更新します
3. 毎日違う言葉が表示されます

## 📊 CSVファイルの形式

```csv
言葉,話されている国（国旗）,日本語読み,日本語の意味
Hello,🇺🇸 English (アメリカ),ハロー,こんにちは
Bonjour,🇫🇷 French (フランス),ボンジュール,こんにちは
Hola,🇪🇸 Spanish (スペイン),オラ,こんにちは
Guten Tag,🇩🇪 German (ドイツ),グーテン・ターク,こんにちは
Ciao,🇮🇹 Italian (イタリア),チャオ,こんにちは / さようなら
안녕하세요,🇰🇷 Korean (韓国),アンニョンハセヨ,こんにちは
你好,🇨🇳 Chinese (中国),ニーハオ,こんにちは
Привет,🇷🇺 Russian (ロシア),プリヴィエット,こんにちは
```

## ⚙️ セットアップ

1. このリポジトリをフォークまたはクローン
2. `data/words.csv` ファイルを作成し、学習したい言葉を追加
3. GitHub Actionsが自動的に毎日更新します

## 🤖 自動更新

- **更新時間**: 毎日 09:00 JST
- **更新方法**: GitHub Actions による自動コミット
- **同じ日なら同じ言葉**: 日付ベースのシード値を使用

---

*最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} JST*

*This README is automatically updated daily by GitHub Actions* 🚀
"""
    
    return readme_content

def update_readme():
    """README.mdを更新"""
    # 今日の言葉を取得
    word_data = get_todays_word()
    
    # README.mdの内容を生成
    readme_content = create_readme_content(word_data)
    
    # README.mdファイルに書き込み
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("README.md を正常に更新しました")
        
        if word_data:
            print(f"今日の言葉: {word_data['word']} ({word_data['meaning']})")
        
    except Exception as e:
        print(f"README.md の更新中にエラーが発生しました: {e}")

if __name__ == "__main__":
    update_readme()
