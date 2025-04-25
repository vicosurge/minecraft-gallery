import markdown

with open("carcosa.md", "r", encoding="utf-8") as f:
    text = f.read()

html = markdown.markdown(text)

with open("carcosa.html", "w", encoding="utf-8") as f:
    f.write(html)
