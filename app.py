import gradio as gr
from dotenv import load_dotenv

load_dotenv()


def greet(name: str) -> str:
    return f"Hello, {name}!"


with gr.Blocks() as demo:
    gr.Markdown("## welcome vibecode starter")

    name_input = gr.Textbox(label="Your name")
    greet_btn = gr.Button("Greet")
    output = gr.Textbox(label="Output", interactive=False)

    greet_btn.click(fn=greet, inputs=name_input, outputs=output)

demo.launch(
    theme=gr.themes.Soft(),
    css=".my-class { color: red; }",
)
