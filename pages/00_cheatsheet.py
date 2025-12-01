import streamlit as st

icon = "https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg"

st.set_page_config(page_title="Markdown Cheat Sheet", page_icon=icon)

st.logo(icon, link="https://github.com/gfm/")
st.markdown("### Markdown Cheat Sheet")
left, right = st.columns(2)

left.markdown("**:memo: テキスト書式**")
left.markdown("""
要素 | :green[HTML] | 用法
--- | --- | ---
見出し1 | `<h1>見出し1</h1>` | `# 見出し1`
見出し2 | `<h2>見出し2</h2>` | `## 見出し2`
太字 | `<strong>太字</strong>` | `**太字**`
斜体 | `<em>斜体</em>` | `*斜体*`
打ち消し線 | `<del>打ち消し線</del>` | `~~打ち消し線~~`
引用 | `<blockquote>引用</blockquote>` | `> 引用`
コード | `<code>コード</code>` | `` `コード` ``
改行 | `<br>` | `行末に2つ以上のスペース`
段落 | `<p>段落</p>` | 空行
ESC | `--` | `¥¥`
""")

with right:
    st.markdown("**:material/format_list_bulleted: リスト**")
    st.markdown("""
要素 | :green-background[HTML] | 用法
--- | --- | ---
順序なしリスト | `<ul><li>項目1</li><li>` | `-`
順番付きリスト | `<ol><li>項目1</li><li>` | `1.`
""")

    with st.expander("**リンク**", icon="🔗", expanded=True):
        st.markdown("""
要素 | :green-background[HTML] | 用法
--- | --- | ---
リンク | `<a href=...>` | `[文字列](URL)`
画像 | `<img src=...>` | `![代替テキスト](URL)`
""")

with right.expander("**表**", icon="📊", expanded=True):
    st.markdown("""
ヘッダ1 | ヘッダ2 | ヘッダ3
--- | --- | ---
行1セル1 | 行1セル2 | 行1セル3
行2セル1 | 行2セル2 | 行2セル3
行3セル1 | 行3セル2 | 行3セル3
""")
