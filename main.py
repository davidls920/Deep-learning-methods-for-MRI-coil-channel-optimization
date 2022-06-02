from NNs import *
from ROVir import *
from methods import *
from pathlib import Path as path
import cv2 as cv
import torchvision.transforms as T

WEIGHTS_PATH = (path.cwd() / "model" / "FastNN.pth").as_posix()
IMG_PATH = (path.cwd() / "data" / "test.png").as_posix()
IMG_SIZE = 144

model = load_model(WEIGHTS_PATH)

img = cv.imread(IMG_PATH, 0)
w,h = img.shape

print(img.shape)
cv.imshow("test",img)

img = T.ToTensor()(img)
img_ = T.Resize(IMG_SIZE)(img).unsqueeze(0)
bbox_A = model(img_)[0]
bbox_A = convert_bbox(bbox_A, w, h)

img = img.type(torch.uint8)

cv.imshow("test2", img.numpy()[0])
training_result = torchvision.utils.draw_bounding_boxes(
    img,
    bbox_A.unsqueeze(0),
    colors='green',
    width=2
)

show(training_result)
plt.show()

#closing all open windows 
cv.destroyAllWindows() 