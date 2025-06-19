import bbcode

def render_comment_preview(text):
    parser = bbcode.Parser()
    html = parser.format(text)
    return html