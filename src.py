import numpy as np
import cv2
from skimage import io, transform, util
from skimage import filters, color
from seam_carving import seam_carve


def seam_carving(img, f, n=0, direction='vertical'):
    for i in range(n):
        eimg = f(img)
        img = seam_carve(img, eimg, direction, 1)
    return img, eimg


def forward_energy(img):
    height = img.shape[0]
    width = img.shape[1]
    I = color.rgb2gray(img)

    energy = np.zeros((height, width))
    m = np.zeros((height, width))

    U = np.roll(I, 1, axis=0)
    L = np.roll(I, 1, axis=1)
    R = np.roll(I, -1, axis=1)

    cU = np.abs(R - L)
    cL = np.abs(U - L) + cU
    cR = np.abs(U - R) + cU

    for i in range(1, height):
        mU = m[i - 1]
        mL = np.roll(mU, 1)
        mR = np.roll(mU, -1)

        mULR = np.array([mU, mL, mR])
        cULR = np.array([cU[i], cL[i], cR[i]])
        mULR += cULR

        argmins = np.argmin(mULR, axis=0)
        m[i] = np.choose(argmins, mULR)
        energy[i] = np.choose(argmins, cULR)

    return energy
