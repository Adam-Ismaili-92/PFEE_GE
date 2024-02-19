import numpy as np
import SimpleITK as sitk
from skimage.morphology import ball
from skimage.morphology import binary_closing
import cv2
from array import array
import math
import numpy as np

def segmentation_bone_class(volume_data) :
    sitk_img = sitk.GetImageFromArray(volume_data)
    
    # preprocessing
    
    sitk_smoothed_img = sitk.SmoothingRecursiveGaussian(sitk_img, sigma=1) # gaussian blur to reduce noise
    
    # processing / hysteresis thresholding
    
    prepro_arr = sitk.GetArrayFromImage(sitk_smoothed_img)
    seedPoints = np.argwhere(prepro_arr > 500)
    seedPoints = [tuple(array('I', point)) for point in seedPoints]
    
    sitk_segmented_img = sitk.ConnectedThreshold(sitk_smoothed_img,
                                                 seedList=seedPoints,
                                                 lower=200,
                                                 upper=500)
    
    # postprocessing
    
    radius = 3
    sitk_closed_img = sitk.BinaryMorphologicalClosing(sitk_segmented_img, [radius] * 3)
    
    sitk_filled_img = sitk.BinaryFillhole(sitk_closed_img)

    # function to dilate with fractional radius, not working in sitk.BinaryDilate
    
    def dilate_with_fractional_radius(image, fractional_radius):
        integer_radius = int(fractional_radius)
        fractional_part = fractional_radius - integer_radius
    
        dilated_image = sitk.BinaryDilate(image, [integer_radius] * 3)
    
        if fractional_part > 0:
            border_size = int(math.ceil((fractional_part * 2)))
            
            cropped_image = sitk.Crop(dilated_image, [border_size] * 3, [0] * 3)
    
            fractional_dilated = sitk.BinaryDilate(cropped_image, [1] * 3)
            
            dilated_image = sitk.Paste(dilated_image, fractional_dilated, fractional_dilated.GetSize(), [0] * 3)

        return dilated_image

    sitk_contours = sitk.BinaryContour(sitk_filled_img)
    
    sitk_dilated_contours = dilate_with_fractional_radius(sitk_contours, 1.2)
    
    cancellous_bone_segmented = sitk.GetArrayFromImage(sitk_filled_img)
    cortical_bone_segmented = sitk.GetArrayFromImage(sitk_dilated_contours)
    
    bone_segmented = (cancellous_bone_segmented + cortical_bone_segmented).astype("uint8")

    return bone_segmented

def segmentation_tissue_class(volume_data) :
    tissue = np.full(volume_data.shape, -1000)
    tissue[volume_data > -120] = volume_data[volume_data > -120]
    tissue[tissue > -1000] = 1
    tissue[tissue == -1000] = 0
    
    struct = ball(3)

    tissue_morpho = binary_closing(tissue, struct)
    tissue_filled = (tissue_morpho * 255).astype(np.uint8)
    
    for i in range(tissue_filled.shape[2]):
        tissue_filled_i = tissue_filled[:, :, i]
        contour, _ = cv2.findContours(tissue_filled_i, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        contour_mask = np.zeros_like(tissue_filled_i)
    
        for cnt in contour:
            cv2.drawContours(contour_mask, [cnt], 0, 255, -1)
    
        tissue_filled[:, :, i] = np.where(contour_mask > 0, 255, 0)

    tissue_filled = np.where(tissue_filled > 0, 1, 0)
    tissue_segmented = tissue_filled.astype("uint8")

    return tissue_segmented

def segmentation_air_class(volume_data) :
    tissue = np.full(volume_data.shape, -1000)
    tissue[volume_data > -120] = volume_data[volume_data > -120]
    
    tissue[tissue > -1000] = 1
    tissue[tissue == -1000] = 0
    
    struct = ball(3)
    
    tissue_segmented = binary_closing(tissue, struct).astype("uint8")

    return tissue_segmented