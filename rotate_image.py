from PIL import Image
import os

try:
    # Path to the current hero image
    input_path = r"C:\Users\Ryzen 9 5900X\Desktop\Antigravity\el-dorado-site\public\hero-chain.png"
    output_path = r"C:\Users\Ryzen 9 5900X\Desktop\Antigravity\el-dorado-site\public\hero-chain-mobile.png"

    print(f"Opening image from: {input_path}")
    img = Image.open(input_path)
    
    # Rotate 90 degrees clockwise (or -90 to match the CSS rotate(90deg) which is clockwise)
    # CSS rotate(90deg) is usually clockwise. PIL rotate is counter-clockwise.
    # So rotate(-90) in PIL is 90 deg clockwise.
    print("Rotating image...")
    rotated_img = img.rotate(-90, expand=True)
    
    print(f"Saving mobile version to: {output_path}")
    rotated_img.save(output_path)
    print("Success!")

except Exception as e:
    print(f"Error: {e}")
