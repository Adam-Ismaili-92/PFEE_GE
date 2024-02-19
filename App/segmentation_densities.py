import numpy as np

def segmentation_densities(volume_data, segmented_classes) :
    density_water = 0.994
    
    # The voltage used was 60 keV

    atcoeff_mass_cortical_bone = 0.3148
    atcoeff_mass_cancellous_bone = 0.2604 # mean between atcm_water and atcm_cortical_bone, just a feeling
    atcoeff_mass_water = 0.2059
    atcoeff_mass_air = 0.1875

    atcoeff_water = density_water * atcoeff_mass_water

    atcoeff_cortical_bone = np.zeros(segmented_classes.shape)
    atcoeff_cancellous_bone = np.zeros(segmented_classes.shape)
    atcoeff_tissue = np.zeros(segmented_classes.shape)
    atcoeff_air = np.zeros(segmented_classes.shape)
    
    atcoeff_cortical_bone[segmented_classes == 4] = (volume_data[segmented_classes == 4] / 1000) * atcoeff_water + atcoeff_water
    atcoeff_cancellous_bone[segmented_classes == 3] = (volume_data[segmented_classes == 3] / 1000) * atcoeff_water + atcoeff_water
    atcoeff_tissue[segmented_classes == 2] = (volume_data[segmented_classes == 2] / 1000) * atcoeff_water + atcoeff_water
    atcoeff_air[segmented_classes == 1] = (volume_data[segmented_classes == 1] / 1000) * atcoeff_water + atcoeff_water

    density_cortical_bone = atcoeff_cortical_bone / atcoeff_mass_cortical_bone
    density_cancellous_bone = atcoeff_cancellous_bone / atcoeff_mass_cancellous_bone
    density_tissue = atcoeff_tissue / atcoeff_mass_water
    density_air = atcoeff_air / atcoeff_mass_air

    return density_cortical_bone + density_cancellous_bone + density_tissue + density_air