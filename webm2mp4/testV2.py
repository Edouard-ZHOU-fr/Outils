import cv2
import time
# import taichi as ti
import numpy as np

# ti.init(arch=ti.gpu)
# @ti.kernel

def print_reussi(reussi):
    reussi = str(reussi)
    # os.system("clear")
    print("\033[1;32;47m"+reussi+"\033[0m")
    pass

def print_c(clignotant):
    clignotant = str(clignotant)
    # os.system("clear")
    print("\033[5;34;42m"+clignotant+"\033[0m", end='\r')
    pass




#############################################################################


input_file = "/home/hongyu/Videos/Screencasts/LaRochelle_P23.webm"
output_file = "/home/hongyu/SETUP/larochelle/1.mp4"



#############################################################################




startTime = time.time()

avi = cv2.VideoWriter_fourcc(*'XVID')
mp4 = cv2.VideoWriter_fourcc(*'MJPG')

cap = cv2.VideoCapture(input_file)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width:",width, "height:", height)



out = cv2.VideoWriter('output.avi',mp4, 30.0, (width, height))

print_c("En train de convertir!!!")


# time.sleep(5)
while(cap.isOpened()):
    drapeau, frame = cap.read()
    if drapeau==True:
        # frame = cv2.flip(frame,0)

        # img = cv2.resize(frame,(640,480)) 
        cv2.imshow('chauque_frame',frame)
        out.write(frame)
    else:
        print_reussi("Terminé les transformations")
        break

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
    # elif(cv2.waitKey(10)>=0): 
    #     cv2.waitKey(0)


cap.release()
out.release()
cv2.destroyAllWindows()

print("--- %.3f seconds ---" % (time.time() - startTime))





