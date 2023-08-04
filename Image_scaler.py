from PIL import Image
import os

# To activate the venv, open VsCode terminal (View/Open View/Terminal)
# cd E:\GIT_ROOT\pythonProject
# if "Get-ExecutionPolicy" is restricted then run "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
# .\venv\Scripts\Activate

def resize_images(input_dir, output_dir, target_size):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all the files in the input directory
    files = os.listdir(input_dir)

    for file in files:
        # Check if the file is an image (JPEG format)
        if file.lower().endswith('.jpg'):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)

            # Open the image
            img = Image.open(input_path)

            # Resize the image while maintaining the aspect ratio
            img.thumbnail(target_size, Image.LANCZOS)

            # Create a blank 1024x1024 white background
            background = Image.new('RGB', target_size, (255, 255, 255))

            # Calculate the center position for the image on the blank background
            left = (target_size[0] - img.width) // 2
            top = (target_size[1] - img.height) // 2

            # Paste the resized image on the blank background
            background.paste(img, (left, top))

            # Save the resized image
            background.save(output_path)

if __name__ == "__main__":
    # Don't just copy paste the path, you need the separators to be double \\
    input_dir = "C:\\Users\\svc_ac-eko-ia\\Desktop\\Stable_Diff_Yonah\\Photos_Walid"
    output_dir = "C:\\Users\\svc_ac-eko-ia\\Desktop\\Stable_Diff_Yonah\\resized_images\\training_images"
    target_size = (1024, 1024)

    resize_images(input_dir, output_dir, target_size)
