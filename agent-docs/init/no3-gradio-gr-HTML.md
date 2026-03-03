# Custom Components with `gr.HTML`

If you wish to create custom HTML in your app, use the `gr.HTML` component. Here's a basic "HTML-only" example:

```python
gr.HTML(value="<h1>Hello World!</h1>")
```

You can also use html-templates to organize your HTML. Take a look at the example below:

```python
gr.HTML(value="John", html_template"<h1>Hello, {{value}}!</h1><p>${value.length} letters</p>")
```

"John" becomes `value` when injected into the template, resulting in:

```html
<h1>Hello, John!</h1><p>4 letters</p>
```

Notice how we support two types of templating syntaxes: `${}` for custom JavaScript expressions, and `{{}}` for Handlebars templating. You can use either or both in your templates - `${}` allows for completely custom JS logic, while Handlebars provides structured templating for loops and conditionals.

Let's look at another example for displaying a list of items:

```python
gr.HTML(value=["apple", "banana", "cherry"], html_templates="""
    <h1>${value.length} fruits:</h1>
    <ul>
      {{#each value}}
        <li>{{this}}</li>
      {{/each}}
    </ul>
""")
```

By default, the content of gr.HTML will have some CSS styles applied to match the Gradio theme. You can disable this with `apply_default_css=False`. You can also provide your own CSS styles via the `css_template` argument as shown in the next example.

Let's build a simple star rating component using `gr.HTML`, and then extend it with more features.

```python
import gradio as gr

with gr.Blocks() as demo:
    three_star_rating = gr.HTML("""
        <h2>Star Rating:</h2>
        <img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>
        <img class='faded' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>
        <img class='faded' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>
    """, css_template="""
        img { height: 50px; display: inline-block; }
        .faded { filter: grayscale(100%); opacity: 0.3; }
    """)

demo.launch()
```
<gradio-app space='gradio/star_rating_simple'></gradio-app>

Note how we used the `css_template` argument to add custom CSS that styles the HTML inside the `gr.HTML` component.

Let's see how the template automatically updates when we update the value.

```python
import gradio as gr

with gr.Blocks() as demo:
    star_rating = gr.HTML(
        value=3,
        html_template="""
        <h2>Star Rating:</h2>
        ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}""", 
        css_template="""
            img { height: 50px; display: inline-block; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """)
    rating_slider = gr.Slider(0, 5, 3, step=1, label="Select Rating")
    rating_slider.change(fn=lambda x: x, inputs=rating_slider, outputs=star_rating)

demo.launch()
```
<gradio-app space='gradio/star_rating_templates'></gradio-app>

We may wish to pass additional props beyond just `value` to the `html_template`. Simply add these props to your templates and pass them as kwargs to the `gr.HTML` component. For example, lets add `size` and `max_stars` props to the star rating component.

```python
import gradio as gr

with gr.Blocks() as demo:
    star_rating = gr.HTML(
        7, 
        size=40,
        max_stars=10,
        html_template="""
        <h2>Star Rating:</h2>
        ${Array.from({length: max_stars}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}""", 
        css_template="""
            img { height: ${size}px; display: inline-block; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """
    )
    rating_slider = gr.Slider(0, 10, step=1, label="Select Rating")
    rating_slider.change(fn=lambda x: x, inputs=rating_slider, outputs=star_rating)

    size_slider = gr.Slider(20, 100, 40, step=1, label="Select Size")
    size_slider.change(fn=lambda x: gr.HTML(size=x), inputs=size_slider, outputs=star_rating)

demo.launch()
```
<gradio-app space='gradio/star_rating_props'></gradio-app>

Note how both `html_template` and `css_template` can format these extra props. Note also how any of these props can be updated via Gradio event listeners.

## Triggering Events and Custom Input Components

The `gr.HTML` component can also be used to create custom input components by triggering events. You will provide `js_on_load`, javascript code that runs when the component loads. The code has access to the `trigger` function to trigger events that Gradio can listen to, and the object `props` which has access to all the props of the component, including `value`.

```python
import gradio as gr

with gr.Blocks() as demo:
    star_rating = gr.HTML(
        value=3, 
        html_template="""
        <h2>Star Rating:</h2>
        ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}
        <button id='submit-btn'>Submit Rating</button>
        """, 
        css_template="""
            img { height: 50px; display: inline-block; cursor: pointer; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """,
        js_on_load="""
            const imgs = element.querySelectorAll('img');
            imgs.forEach((img, index) => {
                img.addEventListener('click', () => {
                    props.value = index + 1;
                });
            });
            const submitBtn = element.querySelector('#submit-btn');
            submitBtn.addEventListener('click', () => {
                trigger('submit');
            });
        """)
    rating_output = gr.Textbox(label="Submitted Rating")
    star_rating.submit(lambda x: x, inputs=star_rating, outputs=rating_output)

demo.launch()
```
<gradio-app space='gradio/star_rating_events'></gradio-app>

Take a look at the `js_on_load` code above. We add click event listeners to each star image to update the value via `props.value` when a star is clicked. This also re-renders the template to show the updated value. We also add a click event listener to the submit button that triggers the `submit` event. In our app, we listen to this trigger to run a function that outputs the `value` of the star rating.

The `js_on_load` scope also includes an `upload` async function that lets you upload a JavaScript `File` object directly to the Gradio server. It returns a dictionary with `path` (the server-side file path) and `url` (the public URL to access the file).

```js
const { path, url } = await upload(file);
```

Here is an example of a custom file-upload widget built with `gr.HTML`:

```python
import gradio as gr
from pathlib import Path

with gr.Blocks() as demo:

    file_uploader = gr.HTML(
        html_template="""
        <div>
            <input type="file" id="file-input" accept=".txt,text/plain" />
            <button id="upload-btn" style="margin-left: 8px;">Upload</button>
        </div>
        """,
        js_on_load="""
        const input = element.querySelector('#file-input');
        const btn = element.querySelector('#upload-btn');

        btn.addEventListener('click', async () => {
            const file = input.files[0];
            const { path } = await upload(file);
            props.value = path;
        });
        """,
        elem_id="file_uploader"
    )

    view_content_btn = gr.Button("View Uploaded File Content")
    upload_content = gr.Textbox(label="Uploaded File Content")

    view_content_btn.click(lambda path: Path(path).read_text(), file_uploader, upload_content)

demo.launch()

```
<gradio-app space='gradio/html_upload'></gradio-app>

You can update any other props of the component via `props.<prop_name>`, and trigger events via `trigger('<event_name>')`. The trigger event can also be send event data, e.g.

```js
trigger('event_name', { key: value, count: 123 });
```

This event data will be accessible the Python event listener functions via gr.EventData.

```python
def handle_event(evt: gr.EventData):
    print(evt.key)
    print(evt.count)

star_rating.event(fn=handle_event, inputs=[], outputs=[])
```

Keep in mind that event listeners attached in `js_on_load` are only attached once when the component is first rendered. If your component creates new elements dynamically that need event listeners, attach the event listener to a parent element that exists when the component loads, and check for the target. For example:

```js
element.addEventListener('click', (e) =>
    if (e.target && e.target.matches('.child-element')) {
        props.value = e.target.dataset.value;
    }
);
```

## Server Functions

You can call Python functions directly from your `js_on_load` code using the `server_functions` parameter. Pass a list of Python functions to `server_functions`, and they become available as async methods on a `server` object inside `js_on_load`.

```python
import os

import gradio as gr


def list_files(path):
    try:
        return os.listdir(path)
    except (FileNotFoundError, PermissionError) as e:
        return [f"Error: {e}"]


with gr.Blocks() as demo:
    gr.Markdown(
        "# Server Functions Demo\nClick 'Load Files' to list files in the directory."
    )
    filetree = gr.HTML(
        value=os.path.dirname(__file__),
        html_template="""
            <div>
                <p>Directory: <strong>${value}</strong></p>
                <div class='tree'></div>
                <button class='load-btn'>Load Files</button>
            </div>
        """,
        js_on_load="""
            const loadBtn = element.querySelector('.load-btn');
            const tree = element.querySelector('.tree');
            loadBtn.addEventListener('click', async () => {
                const files = await server.list_files(props.value);
                tree.innerHTML = '';
                files.forEach(file => {
                    const fileEl = document.createElement('div');
                    fileEl.textContent = file;
                    tree.appendChild(fileEl);
                });
            });
        """,
        server_functions=[list_files],
    )


demo.launch()

```
<gradio-app space='gradio/html_server_functions'></gradio-app>


## Component Classes

If you are reusing the same HTML component in multiple places, you can create a custom component class by subclassing `gr.HTML` and setting default values for the templates and other arguments. Here's an example of creating a reusable StarRating component.

```python
import gradio as gr

class StarRating(gr.HTML):
    def __init__(self, label, value=0, **kwargs):
        html_template = """
        <h2>${label} rating:</h2>
        ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}
        """
        css_template = """
            img { height: 50px; display: inline-block; cursor: pointer; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """
        js_on_load = """
            const imgs = element.querySelectorAll('img');
            imgs.forEach((img, index) => {
                img.addEventListener('click', () => {
                    props.value = index + 1;
                });
            });
        """
        super().__init__(value=value, label=label, html_template=html_template, css_template=css_template, js_on_load=js_on_load, **kwargs)

    def api_info(self):
        return {"type": "integer", "minimum": 0, "maximum": 5}


with gr.Blocks() as demo:
    gr.Markdown("# Restaurant Review")
    food_rating = StarRating(label="Food", value=3)
    service_rating = StarRating(label="Service", value=3)
    ambience_rating = StarRating(label="Ambience", value=3)

    average_btn = gr.Button("Calculate Average Rating")

    rating_output = StarRating(label="Average", value=3)
    def calculate_average(food, service, ambience):
        return round((food + service + ambience) / 3)
    average_btn.click(
        fn=calculate_average,
        inputs=[food_rating, service_rating, ambience_rating],
        outputs=rating_output
    )

demo.launch()

```
<gradio-app space='gradio/star_rating_component'></gradio-app>

Note: Gradio requires all components to accept certain arguments, such as `render`. You do not need
to handle these arguments, but you do need to accept them in your component constructor and pass
them to the parent `gr.HTML` class. Otherwise, your component may not behave correctly. The easiest
way is to add `**kwargs` to your `__init__` method and pass it to `super().__init__()`, just like in the code example above.

We've created several custom HTML components as reusable components as examples you can reference in [this directory](https://github.com/gradio-app/gradio/tree/main/gradio/components/custom_html_components).


## Embedding Components in HTML

The `gr.HTML` component can also be used as a container for other Gradio components using the `@children` placeholder. This allows you to create custom layouts with HTML/CSS. 

The `@children` must be at the top-level of the `html_template`. Since children cannot be nested inside the template, target the parent element directly with your CSS and JavaScript if you need to style or interact with the container of the children.

Here's a basic example:

```python
import gradio as gr

with gr.Blocks() as demo:
    with gr.HTML(html_template='''
        <button class="maximize">&#x26F6;</button>
        <h2>${form_name}</h2>
        @children
        <button class="submit">Submit</button>
    ''', css_template='''
        border: 2px solid gray;
        border-radius: 12px;
        padding: 20px;

        .maximize {
            position: absolute;
            top: 10px;
            right: 10px;
            background: none;
            border: none;
            z-index: 1000;
        }
    ''', js_on_load='''
        element.querySelector('.submit').addEventListener('click', () => {
            trigger('submit');
        });
        element.querySelector('.maximize').addEventListener('click', () => {
            element.requestFullscreen();
        });
    ''', form_name="Custom Form") as form:
        name = gr.Textbox(label="Name")
        email = gr.Textbox(label="Email")

    output = gr.Textbox(label="Output")
    
    form.submit(lambda name, email: f"Name: {name}, Email: {email}", inputs=[name, email], outputs=output)

demo.launch()
```
<gradio-app space='gradio/html_children'></gradio-app>

In this example, the `@children` placeholder marks where the child components (the Name and Email textboxes) will be rendered. Notice how in the `css_template` we target the parent element to style the container div that wraps the children.


### API / MCP support

To make your custom HTML component work with Gradio's built-in support for API and MCP (Model Context Protocol) usage, you need to define how its data should be serialized. There are two ways to do this:

**Option 1: Define an `api_info()` method**

Add an `api_info()` method that returns a JSON schema dictionary describing your component's data format. This is what we do in the StarRating class above.

**Option 2: Define a Pydantic data model**

For more complex data structures, you can define a Pydantic model that inherits from `GradioModel` or `GradioRootModel`:

```python
from gradio.data_classes import GradioModel, GradioRootModel

class MyComponentData(GradioModel):
    items: List[str]
    count: int

class MyComponent(gr.HTML):
    data_model = MyComponentData
```

Use `GradioModel` when your data is a dictionary with named fields, or `GradioRootModel` when your data is a simple type (string, list, etc.) that doesn't need to be wrapped in a dictionary. By defining a `data_model`, your component automatically implements API methods.

## Security Considerations

Keep in mind that using `gr.HTML` to create custom components involves injecting raw HTML and JavaScript into your Gradio app. Be cautious about using untrusted user input into `html_template` and `js_on_load`, as this could lead to cross-site scripting (XSS) vulnerabilities. 

You should also expect that any Python event listeners that take your `gr.HTML` component as input could have any arbitrary value passed to them, not just the values you expect the frontend to be able to set for `value`. Sanitize and validate user input appropriately in public applications.

## Next Steps

Check out some examples of custom components that you can build in [this directory](https://github.com/gradio-app/gradio/tree/main/gradio/components/custom_html_components).