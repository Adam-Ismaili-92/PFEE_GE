import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText  
import sys
from segmentation_pipeline import segmentation_pipeline
import nibabel as nib
import numpy as np
import subprocess
import os

class SegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentation Application")

        self.open_btn = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_btn.pack()

        self.segment_btn = tk.Button(root, text="Segment", command=self.segment_image, state=tk.DISABLED)
        self.segment_btn.pack()

        self.file_path = None

        self.console_output = ScrolledText(root, height=10, width=50, wrap=tk.WORD)
        self.console_output.pack()

        sys.stdout = self.ConsoleRedirector(self.console_output, sys.stdout)
        sys.stderr = self.ConsoleRedirector(self.console_output, sys.stderr)

    def open_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
        if self.file_path:
            self.segment_btn['state'] = tk.NORMAL
            self.print_to_console("Image Loaded: {}".format(self.file_path))

    def segment_image(self):
        if self.file_path:
            try:
                result = segmentation_pipeline(self.file_path)
                self.print_to_console("Segmentation Complete: Segmentation process completed successfully!")

                # Access the segmented classes from the result
                segmented_classes = result.classes
                
                folder_path = "../result/"
                
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Save the segmented classes
                save_path = folder_path + 'segmented_classes.nii.gz'
                segmented_classes_nii = nib.Nifti1Image(segmented_classes, affine=np.eye(4))
                nib.save(segmented_classes_nii, save_path)
                self.print_to_console("Data Saved: Segmented classes saved to '{}'".format(save_path))

                save_path2 = folder_path + 'segmented_densities.nii.gz'
                segmented_densitites = result.densities()
                segmented_densitites_nii = nib.Nifti1Image(segmented_densitites, affine=np.eye(4))
                nib.save(segmented_densitites_nii, save_path2)
                self.print_to_console("Data Saved: Segmented densities saved to '{}'".format(save_path2))

                save_path2 = folder_path + 'segmented_attenuation.nii.gz'
                segmented_attenuation = result.densities(False)
                segmented_attenuation_nii = nib.Nifti1Image(segmented_attenuation, affine=np.eye(4))
                nib.save(segmented_attenuation_nii, save_path2)
                self.print_to_console("Data Saved: Segmented attenuations saved to '{}'".format(save_path2))

                save_path3 = folder_path + 'positions.txt'
                file = open(save_path3, "w")
                i = 0
                for position in result.positions:
                    if (i == 0):
                        file.write(f"Voxel size in meters: {position}\n")
                    if (i == 1):
                        file.write(f"Marker position: {position}\n")
                    i += 1
                print(f"Segmented positions saved to {save_path3}")

                # Display a message in the console
                messagebox.showinfo("Segmentation Complete", "Segmented classes saved successfully!")

            except Exception as e:
                self.print_to_console("Segmentation Failed: {}".format(str(e)))
                messagebox.showerror("Segmentation Failed", str(e))

    def print_to_console(self, message):
        self.console_output.insert(tk.END, message + '\n')
        self.console_output.see(tk.END)

    class ConsoleRedirector:
        def __init__(self, widget, output):
            self.widget = widget
            self.output = output

        def write(self, message):
            self.output.write(message)
            self.widget.insert(tk.END, message)

dependencies = [
    "nibabel",
    "numpy",
    "matplotlib",
    "scipy",
    "scikit-image",
    "Pillow",
    "tk",
    "SimpleITK"
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

    # Initialize Tkinter application
    root = tk.Tk()
    app = SegmentationApp(root)
    root.mainloop()
