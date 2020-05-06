import numpy as np # As open CV relies on numpy
import cv2

''' We want to classify the coins and we will do that by looking at their
 sizes and the brightness of coins in the image.'''
 
img = cv2.imread('capstone-coins.png',cv2.IMREAD_GRAYSCALE) # read the image in Grayscale
original_image = cv2.imread('capstone-coins.png',1) # This is original image with all colours included
 

img = cv2.GaussianBlur(img, (5,5), 0) # If there are too much details in the coin then openCV starts finding circle
                                      #everywhere and we don't want that so we blur image a bit.


''' We use Hough Circle transforms to find circles in the image.'''

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120,
                            param1=50,param2=27,minRadius=60,maxRadius=120) 
# These parameters are the best tuned.
print(circles)
''' We got some coordinates as the output. It found 8 circles. 
If we read the documentation of HoughCircles,
we will know that each circle is described by the three parameters. 
Here, each row corresponds to a different circle.'''

###########################################################################

''' We now draw these circles on our original image. '''

circles = np.uint16(np.around(circles)) # We have rounded the circles result as we have to plot these on our images.
# and In order to do that we need integer values because we don't have decimal pixels on our image.

count = 0
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(original_image,(i[0],i[1]),i[2],(0,255,0),2) # Here (0,255,0) denotes the colour of the circle we want to draw.
    # 2 is the line thickness.
    
    # draw the center of the circle
    cv2.circle(original_image,(i[0],i[1]),2,(0,0,255),3)
    
    #cv2.putText(original_image, str(count),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count += 1
print(count)  

##############################################    ###########################

''' Now, we try to get a list that contains the radii of the coins. 
We create a function that returns the radii value of the circles we created. '''

def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append(coords[2])
    return radius
radii = get_radius(circles) # This list will contain the radius values.
print(radii)

'''We now have the radii of the different circles and therefore the different coins in a list. 
We now look for brightness values so that we can use those two values combined to classify the coins. '''


''' We now write a function to get the brightness. '''

def av_pix(img,circles,size):
    av_value = [] # average value
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size]) # We create a square
        # We're going to get the average value of the pixels or brightness value of the pixels inside that square.
        av_value.append(col)
    return av_value    

bright_values = av_pix(img,circles,20) # We will get square of size 40 by putting 20 here.
print(bright_values)

''' We now have two list. One has radii of the coins and other has the brightness values (from 0 to 255). '''

################# ######################### #############################################

''' Now, we need to put some if conditions to determine which coin is which. '''

# We want to determine the value of the coins based on these two measures - Radii and brightness.
values = []
for a,b in zip(bright_values,radii):
    if a > 150 and b > 110: # If Brightness is above 150 and radius is above 110 then it is 10p coin.
        values.append(10)
    elif a > 150 and b <= 110:
        values.append(5)
    elif a < 150 and b > 110:
        values.append(2)
    elif a < 150 and b < 110:
        values.append(1)        
print(values)           

count_2 = 0
for i in circles[0,:]:
    
    cv2.putText(original_image, str(values[count_2]) + 'p',(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count_2 += 1
cv2.putText(original_image, 'ESTIMATED TOTAL VALUE: ' + str(sum(values)) + 'p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255)


''' We got our expected result as we get total estimated value along with coins value in the coin image. '''

cv2.imshow('Detected Coins',original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

































