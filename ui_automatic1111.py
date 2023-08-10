import gradio as gr # tinker
import subprocess
import os
import shutil

# In the terminal: Ctrl+C to stop running a script

def update_script_and_restart():
    # Specify the paths
    original_script_path = r"E:\GIT_ROOT\pythonProject\Image_Scripts\batch_model_testing.py"
    aut1111_scripts_path = r"E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\scripts"
    aut1111_ui_path = r"E:\GIT_ROOT\AC-EKO-IA\AUTOMATIC1111\webui-user.bat"

    # Copy the script to the AUTOMATIC1111 scripts directory
    new_script_path = os.path.join(aut1111_scripts_path, "batch_model_testing.py")
    shutil.copy(original_script_path, new_script_path)

    # Restart AUTOMATIC1111 UI using subprocess
    subprocess.Popen([aut1111_ui_path], shell=True)

    return "Script updated and AUTOMATIC1111 UI restarted"

ui = gr.Interface(fn=update_script_and_restart, inputs=None, outputs="text", live=True)
ui.launch()