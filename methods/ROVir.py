import numpy as np
from numpy import linalg as LA
from scipy.ndimage import gaussian_filter
from scipy import signal


def ROVir(coils, regions, lowf):
    A_W, A_H, B1_W, B1_H, B2_W = regions

    new_image = np.zeros(coils.shape)
    w = filter_coils(coils)
    tmp_A = w[A_H, A_W, :]
    img_A = tmp_A.flatten().reshape(tmp_A.shape[0]*tmp_A.shape[1], w.shape[2])
    tmp_B = w[B1_H, B1_W, :] + w[B1_H, B2_W, :]
    img_B = tmp_B.flatten().reshape(tmp_B.shape[0]*tmp_B.shape[1], w.shape[2])
    #A = generate_matrix(w[A_H, A_W, :])
    #B = generate_matrix(w[B_H, B_W, :])

    A = generate_matrix(img_A)
    B = generate_matrix(img_B)

    # Calculate eigenvalues and eigenvectors both matrices
    general_matrix = LA.inv(B).dot(A)
    weights = calculate_eig(general_matrix, lowf)
    print(f"{weights=}")

    new_image = coils[:, :, weights]
    print(f"{new_image.shape=}")

    return new_image


def calculate_eig(A, lowf):
    eigenValues, _ = LA.eig(A)
    idx = eigenValues.argsort()[::-1]
    print(f"{eigenValues=}")
    idx = idx[:-lowf]
    return idx


def generate_matrix(imgs):
    matrix = np.zeros((imgs.shape[1], imgs.shape[1]))
    for i in range(imgs.shape[1]):
        for j in range(imgs.shape[1]):
            matrix[i, j] += imgs[:, i].T.dot(imgs[:, j])

    return matrix


def filter_coils(coils):
    new_coils = np.zeros(coils.shape)
    for i in range(coils.shape[2]):
        new_coils[:, :, i] = LA.norm(
            gaussian_filter(coils[:, :, i], sigma=5))

    return new_coils