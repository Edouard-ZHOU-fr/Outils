
#  ########  #######四元数转欧拉角

import numpy as np
import math

def quaternion_to_euler_angle_vectorized1(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))
    return X, Y, Z 


def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]

def degree2Radians(degree):
    return ((degree*math.pi)/180 )

def radians2Degree(radians):
    return ((radians*180)/math.pi )


if __name__ == "__main__":

    # w = 0.7541712712180417 
    # x = 0
    # y = 0
    # z = 0.656677770043545


    x = -0.0042468
    y = 0.027525
    z = 0.99542
    w = 0.091364 




    X,Y,Z = quaternion_to_euler_angle_vectorized1(w,x,y,z)
    
    x_radians = degree2Radians(X)
    y_radians = degree2Radians(Y)
    z_radians = degree2Radians(Z)

    print("\n"+"X(Roll): "+str(X)+" °\nY(Pitch): "+str(Y)+" °\nZ(Yaw): "+str(Z)+" °\n")
    print("\n"+"X(Roll): "+str(x_radians)+" [radians]\nY(Pitch): "+str(y_radians)+
          " [radians]\nZ(Yaw): "+str(z_radians)+" [radians]\n")


