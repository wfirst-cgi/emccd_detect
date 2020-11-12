# -*- coding: utf-8 -*-
"""EMCCD Detector Simulation.

S Miller and B Nemati - UAH - 21-Feb-2020
"""
from __future__ import absolute_import, division, print_function

import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

from emccd_detect.emccd_detect_old import emccd_detect
from emccd_detect.emccd_detect import EMCCDDetect
from emccd_detect.util.imagesc import imagesc

here = os.path.abspath(os.path.dirname(__file__))

# Input fluxmap
fits_name = 'sci_frame.fits'
fits_path = Path(here, 'data', fits_name)
fluxmap = fits.getdata(fits_path)  # Input fluxmap (photons/pix/s)

# Simulation inputs
frametime = 100.  # Frame time (s)
em_gain = 5000.  # CCD EM gain (e-/photon)
full_well_image = 60000.  # Image area full well capacity (e-)
full_well_serial = 100000.  # Serial (gain) register full well capacity (e-)
dark_current = 0.00028  # Dark current rate (e-/pix/s)
cic = 0.01  # Clock induced charge (e-/pix/frame)
read_noise = 100.  # Read noise (e-/pix/frame)
bias = 0.  # Bias offset (e-)
qe = 0.9  # Quantum efficiency
cr_rate = 1.  # Cosmic ray rate (5 for L2) (hits/cm^2/s)
pixel_pitch = 13e-6  # Distance between pixel centers (m)
shot_noise_on = True  # Apply shot noise

sim_im_old = emccd_detect(fluxmap, frametime, em_gain, full_well_image,
                          full_well_serial, dark_current, cic, read_noise,
                          bias, qe, cr_rate, pixel_pitch, shot_noise_on)

# Use class
emccd = EMCCDDetect(
    meta_path=Path(here, 'data', 'metadata.yaml'),
    em_gain=em_gain,
    full_well_image=full_well_image,
    full_well_serial=full_well_serial,
    dark_current=dark_current,
    cic=cic,
    read_noise=read_noise,
    bias=bias,
    qe=qe,
    cr_rate=cr_rate,
    pixel_pitch=pixel_pitch,
    shot_noise_on=shot_noise_on
    )

# Put fluxmap in 1024x1024 image section
image = np.zeros((1024, 1024))
image[0:fluxmap.shape[0], 0:fluxmap.shape[1]] = fluxmap
sim_im = emccd.sim_full_frame(image, frametime)

write_to_file = False
if write_to_file:
    # path = '/Users/sammiller/Documents/GitHub/proc_cgi_frame/data/sim/'
    path = '.'
    fits.writeto(Path(path, 'sim.fits'), sim_im.astype(np.int32),
                 overwrite=True)

# Plot images
plot_images = True
if plot_images:
    for im in [sim_im, sim_im_old]:
        imagesc(fluxmap, 'Input Fluxmap')

        subtitle = ('Gain: {:.0f}   Read Noise: {:.0f}e-   Frame Time: {:.0f}s'
                    .format(em_gain, read_noise, frametime))
        imagesc(im, 'Output Image\n' + subtitle)

    plt.show()
