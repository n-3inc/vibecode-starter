import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APP_TITLE = "My App"

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def update_count(count: int) -> int:
    return count + 1


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """
<h1>${title}</h1>
<p class="count">${value ?? 0}</p>
<button class="btn">+1</button>
"""

CSS_TEMPLATE = """
    text-align: center; padding: 40px;
    .count { font-size: 4rem; font-weight: 800; color: #4c9aff; }
    .btn {
        padding: 8px 24px; border: none; border-radius: 8px;
        background: #4c9aff; color: #fff; cursor: pointer;
    }
"""

JS_ON_LOAD = """
    element.addEventListener('click', function(e) {
        if (e.target.closest('.btn')) {
            props.value = (Number(props.value) || 0) + 1;
        }
    });
"""

GLOBAL_CSS = ""

# ---------------------------------------------------------------------------
# Component Classes (gr.HTML subclass)
# ---------------------------------------------------------------------------


class Badge(gr.HTML):
    def __init__(self, value: str = "", color: str = "#4c9aff", **kwargs):
        super().__init__(
            value=value, color=color,
            html_template='<span class="badge">${value}</span>',
            css_template=".badge { background: ${color}; color: #fff; padding: 2px 12px; border-radius: 12px; font-size: .75rem; font-weight: 700; }",
            **kwargs,
        )


# ---------------------------------------------------------------------------
# Helper Functions (return gr.HTML)
# ---------------------------------------------------------------------------


def create_heading(text: str) -> gr.HTML:
    return gr.HTML(value=text, html_template="<h2>${value}</h2>")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

with gr.Blocks() as demo:
    counter = gr.HTML(
        value="0",
        title=APP_TITLE,
        html_template=HTML_TEMPLATE,
        css_template=CSS_TEMPLATE,
        js_on_load=JS_ON_LOAD,
    )

demo.launch(
    theme=gr.themes.Soft(),
    css=GLOBAL_CSS,
    footer_links=[],
)
