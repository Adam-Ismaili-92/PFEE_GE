import numpy as np


def segmentation_positions(volume_nii, volume_data, segmented_classes) :
    voxel_size = np.array(list(volume_nii.header.get_zooms())) / 1000 # voxel size in meters

    left_upper_body = segmented_classes[:(volume_data.shape[0] // 2), :, int(volume_data.shape[2] / 1.2):]
    
    left_lung = np.zeros_like(volume_data)
    left_lung[:(volume_data.shape[0] // 2), :, int(volume_data.shape[2] / 1.2):] = left_upper_body
    left_lung[left_lung != 1] = 0

    indices = np.where(left_lung == 1)
    nb = indices[0].size
    marker = np.array([np.sum(indices[0]) // nb, np.sum(indices[1]) // nb, np.sum(indices[2]) // nb])

    segmented_positions = (voxel_size, marker)
    
    return segmented_positions