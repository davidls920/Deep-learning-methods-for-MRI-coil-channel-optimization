from methods.neural_network.FastNN import *
from pathlib import Path as path
from methods import *
#from methods.dataset import ChestHeartDataset
#from methods.visualization import *
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn.functional as F
import torchvision.transforms as T
import methods.benchmarking
import cv2 as cv


def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = T.functional.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])


if __name__ == '__main__':
    # Dataset loader
    root_data_path = path.cwd() / 'data' / 'heart_augmented_COCO'
    print(path.cwd())
    training_ann = root_data_path / 'train.json'
    testing_ann = root_data_path / 'test.json'
    validate_ann = root_data_path / 'validation.json'

    train_heart_dataset = ChestHeartDataset(root_data_path, training_ann)
    test_heart_dataset = ChestHeartDataset(root_data_path, testing_ann)
    validate_heart_dataset = ChestHeartDataset(root_data_path, validate_ann)

    net = FastNN().cuda()

    criterion = nn.CrossEntropyLoss()

    batch_size = 32
    training_data_loader = torch.utils.data.DataLoader(
        train_heart_dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    testing_data_loader = torch.utils.data.DataLoader(
        test_heart_dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    validate_data_loader = torch.utils.data.DataLoader(
        validate_heart_dataset,
        batch_size=batch_size,
        shuffle=True,
    )

    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    img, bbox = next(iter(training_data_loader))

    print(type(img))
    print(img.shape)
    # Parameters for training
    epochs = 4
    parameters = filter(lambda p: p.requires_grad, net.parameters())

    optimizer = torch.optim.Adam(
        net.parameters(), lr=0.1
    )

    train_nn(net, epochs, training_data_loader, validate_data_loader,optimizer, device)
    torch.save(net.state_dict(), root_data_path / 'net.pth')
    net.load_state_dict(torch.load(root_data_path / 'net.pth'))

    data_testing(net, testing_data_loader)

    #net = net.to('cpu')

    print("Test image")
    test = cv.imread('test.png', 0)
    test = T.ToTensor()(test)
    print(test.shape)
    test = test.unsqueeze(0)
    print(test.shape)
    test = test.cuda().float()
    bbox_out = net(test)

    print(f'{bbox_out.shape=}')
    test = test.squeeze(0)
    test *= 255
    test = test.type(torch.uint8)
    bbox_out = bbox_out.cpu()
    bbox_out *= 512
    print(f'{bbox_out=}')
    test_boxes = torchvision.utils.draw_bounding_boxes(test, bbox_out, colors='red')
    print(f'{test.shape=}')
    show(test_boxes)
    plt.show()
