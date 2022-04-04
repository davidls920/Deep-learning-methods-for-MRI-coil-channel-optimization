import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from methods import *

dirs = [os.getcwd(), "data", "Slice44-AllChannels.nii"]
data_path = os.path.join(*dirs)

A_W = slice(110, 410)
B1_W = slice(421, -1)
B2_W = slice(0, 50)
A_H = slice(100, 405)
B1_H = slice(100, 350)

DEBUGGING = False

if __name__ == '__main__':
    img = nib.load(data_path)

    height = img.shape[0]
    width = img.shape[1]
    num_coils = img.shape[2]
    # lowf = int(input("lowf = "))
    lowf = 8

    img_np = np.array(img.dataobj)

    prev_img = combine_images(img_np)

    fig, axs = plt.subplots(1, 2)
    regions = [A_W, A_H, B1_W, B1_H, B2_W]

    rovir_coils = ROVir(img_np, regions,  lowf)

    #plot_coils(img_np, 'Real coils')

    if not DEBUGGING:
        new_img = combine_images(rovir_coils)

        plot_coils(rovir_coils, 'Virtual coils')

        im1 = axs[0].imshow(prev_img, cmap='gray')
        axs[0].set_title('Before ROVir')

        im2 = axs[1].imshow(new_img, cmap='gray')
        axs[1].set_title('After ROVir')

        print(f'{np.mean(new_img)=}')

        im1.set_clim(0, 1000)
        im2.set_clim(0, 1500)
    else:
        top5 = combine_images(rovir_coils[:, :, :5])
        bot5 = combine_images(rovir_coils[:, :, -13:])

        im2 = axs[0].imshow(top5, cmap='gray')
        axs[0].set_title('Top 5 coils')

        im3 = axs[1].imshow(bot5, cmap='gray')
        axs[1].set_title('Bottom 5 coils')

        plot_coils(rovir_coils)

        pass

    plt.show()
