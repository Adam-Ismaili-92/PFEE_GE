import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import SimpleITK as sitk
from skimage.morphology import binary_closing, ball
from array import array
import math

from segmentation_pipeline import segmentation_pipeline

def main():
    path = 'volume-0.nii.gz'
    segmentation = segmentation_pipeline(path)
    # Further code to handle the segmentation results

if __name__ == "__main__":
    main()
