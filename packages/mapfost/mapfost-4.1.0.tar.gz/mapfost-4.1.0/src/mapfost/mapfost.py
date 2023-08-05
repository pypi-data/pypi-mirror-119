import os
import requests
import numpy as np
from PIL import Image
from scipy.optimize import minimize

from . import costLib as ctl
from . import mtfLib as mtl
from . import imageLib as iml
from . import costDerivativesLib as cdl
# import costLib as ctl
# import mtfLib as mtl
# import imageLib as iml
# import costDerivativesLib as cdl

def get_mapfost_path():
    return os.path.dirname(__file__)


def est_aberr(test_ims, test_aberrs, pix_size_um=0.08, num_aperture=0.004, stig_rot_deg=0,
              stig_scale=1, use_bessel=False, crop_ref=(0,0), crop_size=(512,512),
              test_ims_aligned=0, get_hessian=False, get_uncertainty=False):
    test_ims_cropped = [
        np.array(Image.fromarray(m).crop((crop_ref[0], crop_ref[1], crop_ref[0] + crop_size[0], crop_ref[1] + crop_size[1]))) for m
        in test_ims]

    if not test_ims_aligned:
        shift_in_meas = [iml.get_shift_vec(test_ims_cropped[0], test_ims_cropped[1]), [0, 0]]
    else:
        shift_in_meas = [[0, 0], [0, 0]]

    for ish in [0,1]:
        if shift_in_meas[0][ish]<0:
            shift_in_meas[1][ish] = shift_in_meas[0][ish]*-1
            shift_in_meas[0][ish] = 0
    all_crop_refS = [[crop_ref[0] + shift_in_meas[k][0],
                      crop_ref[1] + shift_in_meas[k][1],
                      crop_ref[0] + crop_size[0] + shift_in_meas[k][0],
                      crop_ref[1] + crop_size[1] + shift_in_meas[k][1]] for k in [0, 1]]
    cropping_valid = True
    print("all_crop_refS", all_crop_refS)

    if cropping_valid:
        test_ims_cr_al = [np.array(Image.fromarray(m).crop((crop_ref[0] + shift_in_meas[k][0], crop_ref[1] + shift_in_meas[k][1],
                                           crop_ref[0] + crop_size[0] + shift_in_meas[k][0],
                                           crop_ref[1] + crop_size[1]
                                           + shift_in_meas[k][1]))) for k, m in enumerate(test_ims)]

        test_ims_cr_al_pr = [iml.removeMeanAndMeanSlope(im) for im in test_ims_cr_al]
        test_ims_cr_al_pr_fft = [np.fft.fftshift(np.fft.fft2(im)) for im in test_ims_cr_al_pr]
        test_ims_cr_al_pr_fft_lp = [iml.low_pass_filter(m) for m in test_ims_cr_al_pr_fft]

        ps_width, ps_height = test_ims_cr_al_pr_fft_lp[0].shape
        kspace_xy = mtl.get_kspace_xy(ps_width, pix_size_um, stig_rot_deg)

        res = minimize(ctl.cost_mapfost, [0, 0, 0],
                       args=(test_ims_cr_al_pr_fft_lp, test_aberrs, num_aperture,stig_scale, use_bessel, kspace_xy),
                       method="L-BFGS-B")
        res.x = np.round(res.x,2)

        if get_hessian:
            hess_field = cdl.get_hessian_matrix(test_ims_cr_al_pr_fft_lp, np.add(test_aberrs, res.x), num_aperture, pix_size_um)
            res.hess_field = hess_field
            if get_uncertainty:
                res.uncertainty = 1/np.sum(np.diagonal(hess_field**2))

        return res


def test_installation():

    im1 = np.array(Image.open(requests.get('https://gitlab.com/rangolisaxena90/mapfost/-/raw/main/src/mapfost/example/test_im1.png', stream=True).raw))
    im2 = np.array(Image.open(requests.get('https://gitlab.com/rangolisaxena90/mapfost/-/raw/main/src/mapfost/example/test_im2.png', stream=True).raw))
    res = est_aberr([im1, im2], [[-4,0,0],[4,0,0]], get_hessian=True)
    if res.x[0] == -4.21 and res.x[1] ==  -5.72 and res.x[2] ==  1.56:
        print("...Installation Test Successful...")
        print(res)
    else:
        print(".. check if the result is close to the one given in the docs...")
        print(res)


