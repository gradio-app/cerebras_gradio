import os
import gradio as gr
from typing import Callable
from cerebras.cloud.sdk import Cerebras

__version__ = "0.0.1"

def get_fn(model_name: str, preprocess: Callable, postprocess: Callable):
    def fn(message, history):
        # Preprocess the inputs
        inputs = preprocess(message, history)

        # Initialize the Cerebras client for Cerebras
        client = Cerebras(
            api_key=os.environ.get("CEREBRAS_API_KEY"),
        )

        # Call the Cerebras Client with streaming enabled
        completion = client.chat.completions.create(
            model=model_name,
            messages=inputs['messages'],
            stream=True,
        )

        # Streaming response to Gradio ChatInterface UI
        response_text = ""
        for chunk in completion:
            delta = chunk.choices[0].delta.content or ""
            response_text += delta
            yield postprocess(response_text)
    return fn

def get_interface_args(pipeline):
    if pipeline == "chat":
        # Using the default ChatInterface for chat models
        inputs = None
        outputs = None
        def preprocess(message, history):
            # Constructing the messages list from the conversation history
            messages = []
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
            messages.append({"role": "user", "content": message})
            return {'messages': messages}

        postprocess = lambda x: x  # No post-processing needed
    else:
        # Add other pipeline types when they will be needed
        raise ValueError(f"Unsupported pipeline type: {pipeline}")
    return inputs, outputs, preprocess, postprocess

def get_pipeline(model_name):
    # Determine the pipeline type based on the model name
    # For simplicity, assuming all models are chat models at the moment
    return "chat"

def registry(name: str, api_key: str = None, **kwargs):
    """
    Create a Gradio Interface for a model on Cerebras.

    Parameters:
        - name (str): The name of the model on Cerebras.
        - api_key (str, optional): The API key for Cerebras.
    """
    # Ensure the Cerebras API key is set
    api_key = api_key or os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise ValueError("CEREBRAS_API_KEY environment variable is not set.")

    # Determine the pipeline type
    pipeline = get_pipeline(name)
    inputs, outputs, preprocess, postprocess = get_interface_args(pipeline)
    fn = get_fn(name, preprocess, postprocess)

    if pipeline == "chat":
        # Create a Gradio ChatInterface
        interface = gr.ChatInterface(fn=fn, **kwargs)
    else:
        # For other pipelines, create a standard Interface
        interface = gr.Interface(fn=fn, inputs=inputs, outputs=outputs, **kwargs)

    return interface
