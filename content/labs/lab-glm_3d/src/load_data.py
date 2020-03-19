import nibabel as nib
def load_data(filename,filename_mask):
    data = nib.load(filename)
    mask = nib.load(filename_mask)
    return data, mask