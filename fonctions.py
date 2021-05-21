import imageio
import time
import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt


def get_sequence(image, side):
    # Renvoie la bande de l'image originelle ou il y a les verres rouges et le masque de verres rouges dans cette bande
    img2, r = get_red_mask(image)

    for q in [0.05, 0.1, 0.2]:
        # Renvoie le mask des verres vert
        opening = get_green_mask(img2)

        # Dilatation du green mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 500))
        dilatation = cv2.dilate(opening, kernel, iterations=1)

        v = get_final_mask(r, dilatation)
        plt.imshow(v)

        ligne = v[len(v) // 2]

        pattern = get_pattern_1(v, side)

        if pattern_is_valid(pattern, side):
            return pattern

        if not pattern_is_valid(pattern, side):

            pattern = get_pattern_2(v, side)

            if pattern_is_valid(pattern, side):
                return pattern

            if not pattern_is_valid(pattern, side):
                kernel = np.ones((20, 20), np.uint8)
                r = cv2.morphologyEx(r, cv2.MORPH_OPEN, kernel)
                v = get_final_mask(r, opening)

                pattern = get_pattern_2(v, side)
                if pattern_is_valid(pattern, side):
                    return (pattern)

            if not pattern_is_valid(pattern, side):
                ma = 0
                mi = len(ligne)
                for k in range(len(ligne)):
                    if not (ligne[k][0] == 0 and ligne[k][1] == 0 and ligne[k][2] == 0):
                        if (ma < k):
                            ma = k
                        if (mi > k):
                            mi = k
                interval = (ma - mi) // 10
                for j in range(len(v) // 10, len(v), interval):
                    pattern = []
                    ligne = v[j]

                    for k in range(5):

                        if (v[j][mi + interval * (2 * k + 1)][0] == 255):
                            pattern += ['R']
                        if (v[j][mi + interval * (2 * k + 1)][1] == 255):
                            pattern += ['V']

                    if pattern_is_valid(pattern, side):
                        return pattern

    if pattern_is_valid(pattern, side):
        return pattern
    else:
        return 'Echec'


def pattern_is_valid(pattern, side):
    valid_pattern = []
    if (side == 'Y'):
        valid_pattern = [['V', 'R', 'R', 'V', 'R'], ['V', 'R', 'V', 'R', 'R'], ['V', 'V', 'R', 'R', 'R']]
    elif (side == 'B'):
        valid_pattern = [['V', 'R', 'V', 'V', 'R'], ['V', 'V', 'R', 'V', 'R'], ['V', 'V', 'V', 'R', 'R']]
    else:
        print('Side non valide. Codes valides : Y, B')
    if (pattern in valid_pattern):
        return (True)
    else:
        return (False)


def get_red_mask(image):
    max_l = 480
    min_l = 0
    img = copy.deepcopy(image)
    for k in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[k][j][0] > image[k][j][1] * 2 and image[k][j][0] > image[k][j][2] * 2):
                img[k][j] = 255
                if (k < max_l):
                    max_l = k
                if (k > min_l):
                    min_l = k
            else:
                img[k][j] = 0
    i = copy.deepcopy(image)[max_l:min_l]
    r = img[max_l:min_l]
    kernel = np.ones((20, 20), np.uint8)
    r = cv2.morphologyEx(r, cv2.MORPH_OPEN, kernel)
    return (i, r)


def get_green_mask(img2, q=1.1):
    for k in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            if (img2[k][j][1] > img2[k][j][0] * q * 1.5 and img2[k][j][1] > img2[k][j][2] * q):
                img2[k][j] = 255
            else:
                img2[k][j] = 0
    kernel = np.ones((20, 20), np.uint8)
    opening = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
    return (opening)


def get_final_mask(r, dilatation):
    v = copy.deepcopy(dilatation)
    for k in range(len(r)):
        for i in range(len(r[0])):
            if (dilatation[k][i][0] == 255):
                v[k][i] = [0, 255, 0]
            elif (r[k][i][0] == 255):
                v[k][i] = [255, 0, 0]
            else:
                v[k][i] = [0, 0, 0]
    return (v)


def get_pattern_1(v, side):
    c = 0
    for k in range(0, len(v), len(v) // 20):
        pattern = []
        ligne = v[k]
        for e in ligne:
            if (e[0] == 255):
                if (c != 0):
                    pattern += ['R']
                c = 0
            elif e[1] == 255:
                if (c != 1):
                    pattern += ['V']
                c = 1
            else:
                c = 2

        if pattern_is_valid(pattern, side):
            return pattern
    return pattern


def get_pattern_2(map, side):
    ligne = map[len(map) // 2]
    ma = 0
    mi = len(ligne)
    for k in range(len(ligne)):
        if not (ligne[k][0] == 0 and ligne[k][1] == 0 and ligne[k][2] == 0):
            if (ma < k):
                ma = k
            if (mi > k):
                mi = k
    interval = (ma - mi) // 10
    pattern = []
    for j in range(len(v) // 10, len(v), interval):
        pattern = []
        ligne = v[j]

        for k in range(5):

            if (v[j][mi + interval * (2 * k + 1)][0] == 255):
                pattern += ['R']
            if (v[j][mi + interval * (2 * k + 1)][1] == 255):
                pattern += ['V']
        if pattern_is_valid(pattern, side):
            return pattern
    return pattern
