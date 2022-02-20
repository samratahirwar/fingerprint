import cv2 as cv
from glob import glob
import os
import numpy as np
from utils.poincare import calculate_singularities
from utils.segmentation import create_segmented_and_variance_images
from utils.normalization import normalize
from utils.gabor_filter import gabor_filter
from utils.frequency import ridge_freq
from utils import orientation
from utils.crossing_number import calculate_minutiaes
from tqdm import tqdm
from utils.skeletonize import skeletonize


def fingerprint_pipline(input_img):
    thin_image=input_img

    # minutias
    minutias = calculate_minutiaes(thin_image)

    return minutias

results = fingerprint_pipline(cv.imread('res.jpeg',0) )
cv.imwrite('ress'+'.png', results)