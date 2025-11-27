# utility_apps

## 仮想環境を作成(最初だけ)
```
uv init
uv add streamlit
uv add pytz
```

## 仮想環境を作成(git clone直後のみ)
```
uv venv
uv sync
```

## 仮想環境へ入る
```
source .venv/bin/activate
```

## 実行
```
streamlit run main.py
```

## テスト実行
```
python -m unittest tests/test_base_converter.py
```

以上
