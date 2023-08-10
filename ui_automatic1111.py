import gradio as gr

def interface(text_input):
    return f"You entered: {text_input}"

iface = gr.Interface(fn=interface, inputs="text", outputs="text")
iface.launch()

# in the terminal: Ctrl+C to stop running a script