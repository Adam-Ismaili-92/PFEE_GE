import subprocess

dependencies = [
    "nibabel",
    "numpy",
    "matplotlib",
    "scipy",
    "scikit-image",
    "Pillow",
    "tk",
    # Add more dependencies as needed
]

def install_dependencies():
    for dep in dependencies:
        try:
            subprocess.check_call(["pip", "install", dep])
            print(f"Successfully installed {dep}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {dep}")

if __name__ == "__main__":
    print("Installing dependencies...")
    install_dependencies()
    print("All dependencies installed.")
