import coredelta
import thiner 
import ridge_count
import cv2
def dist(a,b):
    return abs(b[0]-a[0])+abs(b[1]-a[1])

def sing(p):
    line=()
    d=p['delta'][0]
    c=p['core']
    m=[]
    mi=[]
    for i in range(len(c)):
        cal=dist(c[i],d)
        if len(m)==0 or m>cal:
            mi=c[i]
    return list(map(int,(d[0],d[1],mi[0],mi[1])))

def run(base,tri,img):
    thiner.thin(base,tri)
    p=coredelta.coredelta(tri,tri)
    #print("SINGULARITY:",p)

    #line=sing(p)
    x1,y1,x2,y2=int(p['core'][0][0]),int(p['core'][0][1]),int(p['delta'][0][0]),int(p['delta'][0][1])
    #x1,y1,x2,y2=82, 201, 238, 301
    print("RIDGE LINE:", x1,y1,x2,y2)
   
    # from PIL import Image, ImageDraw

    # original = Image.open(img)
    # xy = [(x1,y1),(x2,y2),(x2,y2),(x1,y1)]
    # mask = Image.new("L", original.size, 0)
    # draw = ImageDraw.Draw(mask)
    # draw.polygon(xy, fill=255, outline=None)
    # black =  Image.new("L", original.size, 0)
    # result = Image.composite(original, black, mask)

    
    # image = cv2.imread(tri) 
    # image = cv2.line(image, (x1,y1),(x2,y2), (255, 0, 0) , 1) 
    # cv2.imwrite(tri, image)  

    # result.save("2"+img)

    # img2 = cv2.imread(img) 
    # img2 = img2[y1:y2,x1:x2] 
    # cv2.imwrite(img, img2)
    if len(p['core'])>=1 and len(p['delta']) >=1:
        print("NO OF RIDGE BETWEEN:",ridge_count.count_line(tri,( x1,y1,x2,y2),img))
    else:
        print("NO OF RIDGE BETWEEN:",ridge_count.msg(tri,"core/delta not available",img))

# base="8.jpeg"
# img="result.jpeg"
# run(base,img)

import os
filist=os.listdir('./img')
for i in filist:
    print(i)
    try:
        run('./img/'+i,'./try/'+i,'./res/'+i)
    except Exception as e:
        print(str(e))

    print('--------')
# img_dir = './img/*'
# output_dir = './res/'


