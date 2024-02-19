import nibabel as nib
from utilities import print_3_slices
from segmentation_classes import segmentation_bone_class, segmentation_tissue_class, segmentation_air_class
from segmentation_densities import segmentation_densities
from segmentation_positions import segmentation_positions
import numpy as np

def load_volume_data(path) :
    volume_nii = nib.load(path)
    volume_data = volume_nii.get_fdata()

    return volume_nii, volume_data

def segmentation_classes(volume_data) :
    print("- segmenting tissues ...")
    segmented_tissues = segmentation_tissue_class(volume_data)
    print("- finished segmenting tissues")

    print("\n- segmenting bones ...")
    segmented_bones = segmentation_bone_class(volume_data)
    print("- finished segmenting bones")

    print("\n- segmenting air/lungs ...")
    segmented_air = segmentation_air_class(volume_data)
    print("- finished segmenting air/lungs")

    return segmented_tissues + segmented_air + segmented_bones

def segmentation_pipeline(path) :
    print("loading data ...")
    volume_nii, volume_data = load_volume_data(path)
    print("finished loading data\n")

    print("segmenting classes ...")
    segmented_classes = segmentation_classes(volume_data)
    print("finished segmenting classes\n")

    print("segmenting densities ...")
    segmented_densities = segmentation_densities(volume_data, segmented_classes)
    print("finished segmenting densities\n")

    print("segmenting positions ...")
    segmented_positions = segmentation_positions(volume_nii, volume_data, segmented_classes)
    print("finished segmenting positions\n")

    print("instancing segmentation struct to return ...")
    class segmentation :
        def __init__(self, classes, densities, positions):
            self.classes = classes
            self.positions = positions
            self.__densities = densities
        
        def densities(self, b=True) :
            if b :
                return self.__densities

            atcoeff_mass_cortical_bone = 0.3148
            atcoeff_mass_cancellous_bone = 0.2604
            atcoeff_mass_water = 0.2059
            atcoeff_mass_air = 0.1875

            densities_copy = self.__densities.copy()
            
            densities_copy[self.classes == 4] *= atcoeff_mass_cortical_bone
            densities_copy[self.classes == 3] *= atcoeff_mass_cancellous_bone
            densities_copy[self.classes == 2] *= atcoeff_mass_water
            densities_copy[self.classes == 1] *= atcoeff_mass_air

            return densities_copy
    print("finished instancing segmentation struct\n")

    print("segmentation completed !")
    return segmentation(segmented_classes, segmented_densities, segmented_positions)