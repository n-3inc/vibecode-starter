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
            trigger('change');
        }
    });
"""

GLOBAL_CSS = "footer { display: none !important; }"

# ---------------------------------------------------------------------------
# Component Classes (gr.HTML subclass)
# ---------------------------------------------------------------------------

from gradio.events import Dependency

class Badge(gr.HTML):
    def __init__(self, value: str = "", color: str = "#4c9aff", **kwargs):
        super().__init__(
            value=value, color=color,
            html_template='<span class="badge">${value}</span>',
            css_template=".badge { background: ${color}; color: #fff; padding: 2px 12px; border-radius: 12px; font-size: .75rem; font-weight: 700; }",
            **kwargs,
        )

    def api_info(self):
        return {"type": "string", "description": "Badge text content"}
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component


# ---------------------------------------------------------------------------
# Helper Functions (return gr.HTML for updating existing components)
# ---------------------------------------------------------------------------


def create_heading(text: str) -> gr.HTML:
    return gr.HTML(value=text, html_template="<h2>${value}</h2>")


def update_counter(value: str) -> gr.HTML:
    """Return gr.HTML update with new value — preserves other props."""
    return gr.HTML(value=value)


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

with gr.Blocks(title=APP_TITLE) as demo:

    gr.Markdown(f"# {APP_TITLE}")

    counter = gr.HTML(
        value="0",
        title=APP_TITLE,
        html_template=HTML_TEMPLATE,
        css_template=CSS_TEMPLATE,
        js_on_load=JS_ON_LOAD,
    )

    with gr.Row():
        with gr.Column(scale=1):
            reset_btn = gr.Button("🗑️ Reset", variant="stop")

    status = gr.Textbox(label="Status", interactive=False)

    # -- Events -----------------------------------------------------------

    counter.change(
        fn=lambda v: f"Count: {v}",
        inputs=counter,
        outputs=status,
    )

    reset_btn.click(
        fn=lambda: (update_counter("0"), "Reset!"),
        inputs=[],
        outputs=[counter, status],
    )

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(),
        css=GLOBAL_CSS,
        footer_links=[],
    )