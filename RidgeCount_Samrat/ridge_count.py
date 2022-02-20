import numpy as np
import cv2

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

import cv2

def count_line4(img,line,save):
    img=cv2.imread(img)
    plist=get_line(line[0],line[1],line[2],line[3])


    clist=[img[i[0],i[1]][0] for i in plist]
    #print(plist,clist)
    c=0
    # rlist=[i  for i in zip(plist,clist) ]
    # zlist=[i  for i in zip(plist,clist) if i[1]<100]
    for i in clist:
        if i<100:
            c+=1
    # for i in rlist:
    #     if i[1]>100:
    #         img[i[0][::-1]]=(255,0,0)
    #     else:
    #         img[i[0][::-1]]=(0,0,0)
        # print(img[i[0][::-1]],end=",")
    # for i in zlist:
    #     print(i,end=",")
    #     img[i[0][::-1]]=(0,0,255)
    
    cv2.putText(img, str(c), (20,20), cv2.FONT_HERSHEY_SIMPLEX ,0.5, (255,0,0), 1, cv2.LINE_AA) 
    cv2.imwrite(save,img)

    return c#len(zlist)


def count_line3(img,line,save):
    c=0
    img = cv2.imread(img)
    crop_img = img[line[1]:line[3],line[0]:line[2]]
    cv2.imwrite(save,crop_img)
    return c;
#[[line[0],line[1]],[line[2],line[2]]

def count_line2(img,line,save):
    c=0
    
    img = cv2.imread(img)
    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    points = np.array([[[line[0],line[2]],[line[1],line[3]]]])
    #method 1 smooth region
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    #method 2 not so smooth region
    # cv2.fillPoly(mask, points, (255))
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    imgc = img[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    ## crate the white background of the same size of original image
    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    # overlap the resulted cropped image on the white background
    dst = wbg+res
    cv2.imwrite(save,imgc)
    # cv2.imshow("Mask",mask)
    # cv2.imwrite(save, cropped )
    # cv2.imshow("Samed Size Black Image", res)
    # cv2.imshow("Samed Size White Image", dst)
 

    return c;


def count_line(img2,line,save):
    c=0
    read = cv2.imread(img2)
    img = cv2.imread(img2)
    img=cv2.line(img,(line[0],line[1]),(line[2],line[3]),(255, 0, 0) , 2)
    cv2.imwrite(img2,img)
    pline=[]
    x,y=0,0
    for i in img:
        y=0
        for j in i:
            if j[0]>200 and j[1]>200 and j[2]>200:
                pass
            elif j[0]<10 and j[1]<10 and j[2]<10:
                pass
            else:
                pline.append((x,y))
            y+=1
        x+=1

    clist=[]
    for i in range(len(pline)):
        x,y=pline[i][0],pline[i][1]
        clist.append(read[x,y])
        if clist[i][0]<100:
            c+=1
            #cv2.circle(read, (pline[i][1],pline[i][0]), 1, (255,0,0), 2)
            read[x,y]=(0,0,255)
            exis=[(x,y+1),(x+1,y),(x+1,y+1),(x+1,y-1),(x-1,y),(x-1,y-1),(x,y-1),(x-1,y+1)]
            for j,k in exis:
                print(j,k)
                if read[x,y]==read[j,k]:
                    read[j,k]=(0,0,0)
    # print(clist)
 
    cv2.circle(read, (line[0],line[1]), 2, (255,0,0), 2)
    cv2.circle(read, (line[2],line[3]), 2, (0,255,0), 2)
    #cv2.line(read,(line[0],line[1]),(line[2],line[3]),(255, 0, 0) , 1)
    cv2.putText(read, str(c), (20,20), cv2.FONT_HERSHEY_SIMPLEX ,0.5, (255,0,0), 1, cv2.LINE_AA) 
    cv2.imwrite(save,read)
    return c;

def msg(img2,line,save):
    read = cv2.imread(img2)
    cv2.putText(read,line, (20,20), cv2.FONT_HERSHEY_SIMPLEX ,0.5, (255,0,0), 1, cv2.LINE_AA) 
    cv2.imwrite(save,read)
    