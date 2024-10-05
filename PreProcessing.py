import ants
from nilearn import masking
import nibabel as nib
import numpy as np
import subprocess
import os

def preproccess(path, serial=None):
    try:
        t1_image_nib = nib.load(path)
    except Exception as e:
        print(f"Error loading NIfTI file: {e}")
        return
    t1_image_data = t1_image_nib.get_fdata()
    t1_image_nib=ants.from_numpy(t1_image_data)
    template = ants.image_read(ants.get_ants_data('mni'))
    registration = ants.registration(fixed=template, moving=t1_image_nib, type_of_transform='Rigid')
    normalized_image = registration['warpedmovout']

    origin = normalized_image.origin
    spacing = normalized_image.spacing
    direction = normalized_image.direction
    affine_matrix = np.eye(4)
    affine_matrix[:3, :3] = np.diag(spacing) @ direction
    affine_matrix[:3, 3] = origin

    normalized_image_np = normalized_image.numpy()
    normalized_image_final=nib.Nifti1Image(normalized_image_np,affine=affine_matrix) 
    print('normalized')
    normalized_image_path = 'C:\\Users\\Pillow\\normalized_image.nii.gz'
    nib.save(normalized_image_final, normalized_image_path)
    
    try:
        subprocess.run(['wsl', f'/mnt/c/Users/Pillow/run_bet.sh'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running FSL BET: {e}")
        return
    
    brain_extracted_path = 'C:\\Users\\Pillow\\brain_extracted_image.nii.gz'
    brain_extracted_image_nib=nib.load(brain_extracted_path)
    brain_extracted_data = brain_extracted_image_nib.get_fdata()
    brain_extracted_ants = ants.from_numpy(brain_extracted_data, origin=origin, spacing=spacing, direction=direction)

    os.remove(normalized_image_path)
    os.remove('C:\\Users\\Pillow\\brain_extracted_image.nii.gz')

    bias_corrected = ants.n4_bias_field_correction(brain_extracted_ants)
    print('bias correct')
    return nib.Nifti1Image(bias_corrected.numpy(),affine=brain_extracted_image_nib.affine).get_fdata()
    ants.image_write(bias_corrected,f'./New_Processed/{serial}.nii.gz')
    print(f"Saved {serial}")
