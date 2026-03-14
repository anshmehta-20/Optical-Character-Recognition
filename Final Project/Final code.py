#DEV CODE:

#9 ways to manipulate image:
# 1. Inverted Image
# 2. Rescaling
# 3. Binarization
# 4. Noise Removal
# 5. Dilation and Erosion
# 6. Rotation / Deskewing
# 7. Removing Borders
# 8. Missing Borders
# 9. Transparency / Alpha Channel

# Opening an image
import cv2
from matplotlib import pyplot as plt
im_file = 'C:\Python Programming\Optical Character Recognition\Final Project\image_01.png'
img = cv2.imread(im_file)

# cv2.imshow("original image", img)
cv2.waitKey(0)


def display(im_path):
    dpi = 80 #Dots per inch
    im_data = cv2.imread(im_path) #Stores numpy.ndarray in im_data
    height, width, depth = im_data.shape #Returns array size: (l,b,h) and stores it in height,width and depth

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

# Inverted Image

inverted_image = cv2.bitwise_not(img)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\inverted_image.png", inverted_image)
# display("D:\Coding\Python\CSE100 Project\inverted_image.png")

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

grayimage = grayscale(img)
cv2.imwrite('C:\Python Programming\Optical Character Recognition\Final Project\grayimage.png', grayimage)
# display('D:\Coding\Python\CSE100 Project\grayimage.png')

thresh, im_bw = cv2.threshold(grayimage, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite('C:\Python Programming\Optical Character Recognition\Final Project\im_bw.png', im_bw)

# Noise Removing
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations = 1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations = 1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

no_noise = noise_removal(im_bw)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\no_noise.png", no_noise)
# display("D:\Coding\Python\CSE100 Project\no_noise.png")

# #ANSH CODE:

def thin_font (image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones ((3,3), np.uint8)
    image = cv2.erode(image, kernel, iterations = 1)
    image = cv2.bitwise_not(image)
    return(image)

eroded_image = thin_font(no_noise)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\eroded_image.png", eroded_image)
# display('D:\Coding\Python\CSE100 Project\img5.png')

# #DEV CODE:
def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations = 1)
    image = cv2.bitwise_not(image)
    return (image)
dilated_image = thick_font(no_noise)
cv2.imwrite('C:\Python Programming\Optical Character Recognition\Final Project\dilated_image.png', dilated_image)



#Rotation / Deskewing:

# new = cv2.imread("img_rotated_path")
new = cv2.imread("C:\Python Programming\Optical Character Recognition\Final Project\image01.png")
def getSkewAngle(cvImage) -> float:
    # Prepare image, copy, convert to gray scale, blurr, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply dilate to merge text into meaningful lines/ paragraphs.
# Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
# But use smaller kernel on Y axis to separate between different blocks of text

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations = 2)

# Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(newImage, (x,y), (x+w, y+h), (0,255,0), 2)

# Find largest contour and surround in min area box
    largestContour = contours[0]
    print(len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\boxes_img.png", newImage)

# Detremine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = angle + 90
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)
    return newImage

def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)
fixed = deskew(new)
cv2.imwrite('C:\Python Programming\Optical Character Recognition\Final Project\rotated_fixed.png', fixed)

# Removing Borders
def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)
no_borders = remove_borders(no_noise)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\no_borders.png", no_borders)
# display('D:\Coding\Python\CSE100 Project\no_borders.png')

# Missing Borders
color = [255, 255, 255]
top, bottom, left, right = [150]*4
image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\image_with_border.png", image_with_border)
# display("D:\Coding\Python\CSE100 Project\image_with_borders.png")

# ***********  Video 5 & 6: Muntazir *************
#
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Python Programming\Optical Character Recognition\Final Project\tesseract.exe"

img_file = "C:\Python Programming\Optical Character Recognition\Final Project\page_1.png"
# no_noise = "D:\Coding\Python\CSE100 Project\no_noise.png"

img = Image.open(img_file)
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)

# # ***********  Video 7: Ansh *************

import pytesseract
import cv2
image = cv2.imread("C:\Python Programming\Optical Character Recognition\Final Project\image01.png")
base_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\grayimage.png", gray)
blur = cv2.GaussianBlur(gray, (7,7), 0)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\blur.png", blur)
thresh = cv2. threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\thresh.png", thresh)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
cv2. imwrite("C:\Python Programming\Optical Character Recognition\Final Project\kernal.png", kernal)
dilate = cv2.dilate(thresh, kernal, iterations=1)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\dilated_image.png", dilate)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2. boundingRect(x) [0])
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    roi = image[y:y+h, x:x+h]
    cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\roi.png", roi)
    cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
cv2. imwrite("C:\Python Programming\Optical Character Recognition\Final Project\box_new.png", image)

# ***********  Video 8: Shashwat *************

result =[]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+h]
        cv2.rectangle(image, (x,y),(x+w,y+h), (36,255,12), 2)
        ocr_result = pytesseract.image_to_string(roi)
        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            result.append(item)
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\box_new.png", image)
print(result)

entities = []
for items in result:
    item = item.strip()
    item = item.split(" ")[0]
    if len(item) > 2:
        if item[0] == "A" and "_" not in item:
            item = item.split(".")[0].replace(",","").replace(";","")
            entities.append(item)
print(entities)

entities = list(set(entities))
print(entities)

entities.sort()
print(entities)

# ***********  Video 9: Dev *************

import pytesseract
import cv2

image = cv2.imread("C:\Python Programming\Optical Character Recognition\Final Project\image01.png")
im_h, im_w, im_d = image.shape
base_image = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]

# Creating rectangular structuring element and dilate
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
dilate = cv2.dilate(thresh, kernal, iterations=1)

# Find contours and draw rectangle
cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\dilated_image.png",dilate)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 250:
        roi = base_image[0:y+h, 0:x+im_w]
        cv2.rectangle(image, (x,y), (x+y, y+h), (36, 255, 12), 2)

cv2.imwrite("C:\Python Programming\Optical Character Recognition\Final Project\output_image.png", image)
# cv2.imshow("Output Image", image)
cv2.waitKey(1)
ocr_result_original = pytesseract.image_to_string(base_image)
print(ocr_result_original)