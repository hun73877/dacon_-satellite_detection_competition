import cv2 as cv
import numpy as np


bins = np.arange(256).reshape(256,1)


def draw_histogram(img):

    h = np.zeros((img.shape[0], 513), dtype=np.uint8)

    hist_item = cv.calcHist([img],[0],None,[256],[0,256])
    cv.normalize(hist_item,hist_item,0,255,cv.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv.line(h,(x,0+10),(x,y+10),(255,255,255))

    cv.line(h, (0, 0 + 10), (0, 5), (255, 255, 255) )
    cv.line(h, (255, 0 + 10), (255, 5), (255, 255, 255))
    y = np.flipud(h)

    #draw curve
    hist, bin = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    cv.normalize(cdf_normalized, cdf_normalized, 0, 255, cv.NORM_MINMAX)
    hist = np.int32(np.around(cdf_normalized))
    pts = np.int32(np.column_stack((bins, hist)))
    pts += [257, 10]

    cv.line(h, (0+257, 0 + 10), (0+257, 5), (255, 255, 255) )
    cv.line(h, (255+257, 0 + 10), (255+257, 5), (255, 255, 255))
    cv.polylines(h, [pts], False, (255,255,255))

    return y


img = cv.imread('../images/228.png', cv.IMREAD_COLOR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


line =  draw_histogram(gray)
result1 = np.hstack((gray, line))
# cv.imshow('hist_result1.png', result1)


# equ = cv.equalizeHist(gray)

hist, bin = np.histogram(img.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_mask = np.ma.masked_equal(cdf,0)
cdf_mask = (cdf_mask - cdf_mask.min())*255/(cdf_mask.max()-cdf_mask.min())
cdf = np.ma.filled(cdf_mask,0).astype('uint8')
equ = cdf[gray]


line =  draw_histogram(equ)
result2 = np.hstack((equ, line))
# cv.imshow('hist_result2', result2)
cv.imwrite('result/hist_result2.png', result2)


cv.waitKey(0)
cv.destroyAllWindows()