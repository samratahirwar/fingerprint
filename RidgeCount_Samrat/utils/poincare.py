from utils import orientation
import math
import cv2 as cv
import numpy as np
count=0
core=None
delta=None

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def poincare_index_at(i, j, angles, tolerance):
    """
    compute the summation difference between the adjacent orientations such that the orientations is less then 90 degrees
    https://books.google.pl/books?id=1Wpx25D8qOwC&lpg=PA120&ots=9wRY0Rosb7&dq=poincare%20index%20fingerprint&hl=pl&pg=PA120#v=onepage&q=poincare%20index%20fingerprint&f=false
    :param i:
    :param j:
    :param angles:
    :param tolerance:
    :return:
    """
    cells = [(-1, -1), (-1, 0), (-1, 1),         # p1 p2 p3
            (0, 1),  (1, 1),  (1, 0),            # p8    p4
            (1, -1), (0, -1), (-1, -1)]          # p7 p6 p5

    angles_around_index = [math.degrees(angles[i - k][j - l]) for k, l in cells]
    index = 0
    for k in range(0, 8):

        # calculate the difference
        difference = angles_around_index[k] - angles_around_index[k + 1]
        if difference > 90:
            difference -= 180
        elif difference < -90:
            difference += 180

        index += difference

    if 180 - tolerance <= index <= 180 + tolerance:
        return "loop"
    if -180 - tolerance <= index <= -180 + tolerance:
        return "delta"
    if 360 - tolerance <= index <= 360 + tolerance:
        return "whorl"
    return "none"


def calculate_singularities(im, angles, tolerance, W, mask):
    global count
    global core
    global delta
    core=None
    delta=None
    count=0
    result = cv.cvtColor(im, cv.COLOR_GRAY2RGB)

    # DELTA: RED, LOOP:ORAGNE, whorl:INK
    colors = {"loop" : (255, 0, 0), "delta" : (0,255,0), "whorl": (255, 153, 255)}

    for i in range(3, len(angles) - 2):             # Y
        for j in range(3, len(angles[i]) - 2):      # x
            # mask any singularity outside of the mask
            mask_slice = mask[(i-2)*W:(i+3)*W, (j-2)*W:(j+3)*W]
            mask_flag = np.sum(mask_slice)
            if mask_flag == (W*5)**2:
                singularity = poincare_index_at(i, j, angles, tolerance)
                if singularity != "none":
                    #print(">>",j*W,i*W,count)
                    if count==0:
                        #print("Core=(",j*W,",",i*W,")")
                        core=(j*W,i*W)
                    if count==3:
                        core=((core[0]+j*W)//2,(core[1]+i*W)//2)
                    if count>3:
                        print("Delta=(",j*W,",",i*W,")")
                        delta=(j*W,i*W)
                    count=count+1
    if core!=None:
        cv.circle(result,core,2,colors["loop"],2)
    if delta!=None:
        cv.circle(result,delta,2,colors["delta"],2)
    if core!=None and delta!=None:
        print(core,delta)
        pix=get_line(core[0],core[1],delta[0],delta[1])
        # l=[]
        # for i in pix[:-1]:
        #     try:
        #         l.append(result[i][0])
        #     except:
        #         l.append(result[reversed(i)][0])
            
        # print(l.count(0),len(pix),len(l))
        # cv.putText(result,str(l.count(0)),(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv.LINE_AA )
        cv.line(result,core,delta,(0,0,255),1)

    else:
        print("core or delta is missing!!!")
    
    return result



if __name__ == '__main__':
    img = cv.imread('../test_img.png', 0)
    cv.imshow('original', img)
    angles = orientation.calculate_angles(img, 16, smoth=True)
    result = calculate_singularities(img, angles, 1, 16)
