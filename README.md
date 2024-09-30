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

Just like if you were to use the `Cerebras` client, you should first save your Cerebras API token to this environment variable:

```
export CEREBRAS_API_KEY=<your api key>
```

Then in a Python file, write:

```python
import gradio as gr
import cerebras_gradio

gr.load(
    name='llama3.1-8b',
    src=cerebras_gradio.models
).launch()
```

Run the Python file, and you should see a Gradio Chat UI connected to the model on Cerebras!



# Customization 

Once you can create a Gradio UI from a cerebras endpoint, you can customize it by setting your own title or examples, or any other arguments to `gr.ChatInterface`. For example, the screenshot above was generated with:

```py
import gradio as gr
import cerebras_gradio

gr.load(
    name='llama3.1-70b',
    src=cerebras_gradio.models
).launch()
```


# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import cerebras_gradio

with gr.Blocks() as demo:
    with gr.Tab("SDXL"):
        gr.load('llama3.1-70b', src=cerebras_gradio.models)
    with gr.Tab("Flux"):
        gr.load('llama3.1-8b', src=cerebras_gradio.models)

demo.launch()
```

# Under the Hood

The `cerebras-gradio` Python library has two dependencies: `cerebras` and `gradio`. It defines a "registry" function `cerebras_gradio.registry`, which takes in a model name and returns a Gradio app.

-------

Note: if you are getting an authentication error, then the cerebras API Client is not able to get the API token from the environment variable. This happened to me as well, in which case save it in your Python session, like this:

```py
import os

os.environ["CEREBRAS_API_KEY"] = ...
```
