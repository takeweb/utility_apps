# utility_apps

## 仮想環境を作成(最初だけ)
```
uv init
uv add streamlit
uv add pytz
```

## 仮想環境へ入る
```
source .venv/bin/activate
```

## 仮想環境内にpyproject.tomlに書かれている依存関係全てを適用(最初だけ)
```
uv sync
```

## 実行
```
streamlit run main.py
```

## Streamlit Community Cloudにデプロイする為に、requirements.txtを生成
```
uv export --format 'requirements-txt' > requirements.txt
```

以上
