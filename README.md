# `cerebras_gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by cerebras's Inference API.

# Installation

1. Clone this repo: `git clone git@github.com:gradio-app/cerebras-gradio.git`
2. Navigate into the folder that you cloned this repo into: `cd cerebras-gradio`
3. Install this package: `pip install -e .`

<!-- ```bash
pip install cerebras-gradio
``` -->

That's it! 

# Basic Usage

Just like if you were to use the `cerebras` client, you should first save your cerebras API token to this environment variable:

```
export cerebras_API_TOKEN=<your token>
```

Then in a Python file, write:

```python
import gradio as gr
import cerebras_gradio

gr.load(
    name='black-forest-labs/flux-schnell',
    src=cerebras_gradio.registry
).launch()
```

Run the Python file, and you should see a Gradio Interface connected to the model on cerebras!

<img width="1246" alt="image" src="https://github.com/user-attachments/assets/2c975cbd-965f-4967-9468-d791aabfc9aa">


# Customization 

Once you can create a Gradio UI from a cerebras endpoint, you can customize it by setting your own input and output components, or any other arguments to `gr.Interface`. For example, the screenshot above was generated with:

```py
import gradio as gr
import cerebras_gradio

gr.load(
    name='black-forest-labs/flux-schnell',
    src=cerebras_gradio.registry,
    inputs=gr.Textbox(lines=4),
    examples=["a 19th century portrait of a man on the moon", "a small cartoon mouse eating an ice cream cone"],
).launch()
```


# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import cerebras_gradio

with gr.Blocks() as demo:
    with gr.Tab("SDXL"):
        gr.load('cerebras-ai/fast-sdxl', src=cerebras_gradio.registry)
    with gr.Tab("Flux"):
        gr.load('black-forest-labs/flux-schnell', src=cerebras_gradio.registry)

demo.launch()
```

# Under the Hood

The `cerebras-gradio` Python library has two dependencies: `cerebras` and `gradio`. It defines a "registry" function `cerebras_gradio.registry`, which takes in a model name and returns a Gradio app.

-------

Note: if you are getting a 401 authentication error, then the cerebras API Client is not able to get the API token from the environment variable. This happened to me as well, in which case save it in your Python session, like this:

```py
import os

os.environ["cerebras_API_TOKEN"] = ...
```
