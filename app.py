import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APP_TITLE = "My App"

# ---------------------------------------------------------------------------
# Server Functions (Javascript から呼び出される Python 関数)
# ---------------------------------------------------------------------------

def server_func(text: str) -> dict:
    return {"result": text}


# ---------------------------------------------------------------------------
# Functions (gr.blocks 内のイベントで呼び出される Python 関数)
# ---------------------------------------------------------------------------

def apply_settings(title: str, description: str) -> gr.HTML:
    """設定パネルの値をカードの props に反映する"""
    return gr.HTML(title=title or "Title", value=description)


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """
<div class="card">
    <h2 class="title">${title}</h2>
    <p class="value">${value}</p>
    <input type="text" class="text-input" placeholder="テキストを入力…" />
    <button class="js-btn">送信</button>
    <p class="rpc-result"></p>
</div>
"""

CSS_TEMPLATE = """
    .card {
        text-align: center; padding: 48px 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px; color: #fff;
        min-height: 200px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .title { font-size: 2.5rem; font-weight: 700; margin: 0 0 24px; }
    .value { font-size: 2rem; margin: 0 0 32px; }
    .text-input {
        font-size: 1rem; padding: 10px 20px; border: 2px solid rgba(255,255,255,0.5);
        border-radius: 999px; background: rgba(255,255,255,0.15); color: #fff;
        outline: none; width: 280px; text-align: center; margin: 0 0 16px;
        transition: border-color 0.2s ease;
    }
    .text-input::placeholder { color: rgba(255,255,255,0.6); }
    .text-input:focus { border-color: #fff; }
    .js-btn {
        font-size: 1rem; padding: 10px 28px; border: 2px solid #fff;
        border-radius: 999px; background: transparent; color: #fff; cursor: pointer;
        transition: transform 0.15s ease;
    }
    .js-btn:hover { transform: scale(1.05); background: rgba(255,255,255,0.15); }
    .rpc-result {
        font-size: 1.1rem; margin: 16px 0 0; min-height: 1.5em; opacity: 0.9;
    }
"""

# JS → Python: server.関数名() で Python 関数を直接呼び出し、戻り値を受け取る
JS_ON_LOAD = """
    element.addEventListener('click', async (e) => {
        if (e.target.closest('.js-btn')) {
            const btn = e.target.closest('.js-btn');
            const input = element.querySelector('.text-input');
            const result = element.querySelector('.rpc-result');
            btn.textContent = '通信中…';
            const response = await server.server_func(input.value || '');
            result.textContent = `結果: ${response.result}`;
            btn.textContent = '送信';
        }
    });
"""

GLOBAL_CSS = "footer { display: none !important; }"

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

with gr.Blocks(title=APP_TITLE) as demo:

    gr.Markdown(f"# {APP_TITLE}")

    with gr.Row():
        with gr.Column(scale=2):
            card = gr.HTML(
                title="Title",
                value="Description",
                html_template=HTML_TEMPLATE,
                css_template=CSS_TEMPLATE,
                js_on_load=JS_ON_LOAD,
                server_functions=[server_func],
            )

        with gr.Column(scale=1):
            gr.Markdown(f"# Settings")
            title_input = gr.Textbox(label="タイトル", value="Title", placeholder="カードのタイトル")
            desc_input = gr.Textbox(label="説明文", value="Description", placeholder="カードの説明文")
            apply_btn = gr.Button("更新", variant="primary")


    # -- Events -----------------------------------------------------------

    # Gradio イベント: 設定パネルの値で card の props（title, value）を更新
    apply_btn.click(
        fn=apply_settings,
        inputs=[title_input, desc_input],
        outputs=card,
    )

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(),
        css=GLOBAL_CSS,
        footer_links=[],
    )
