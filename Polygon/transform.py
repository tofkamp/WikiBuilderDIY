
import math

class Transform:
    def __init__(self):
        self.originX = 0
        self.originY = 0
        self.originZ = 0
        self.quaternion = self._euler_to_quaternion(0,0,0)

    def Move(self,dx,dy,dz):
        self.originX += dx
        self.originY += dy
        self.originZ += dz
        
    # the following quaternions functions do not need a reference to its own object, but else it wont' find the functions
    # https://stackoverflow.com/questions/4870393/rotating-coordinate-system-via-a-quaternion
    def _q_conjugate(self,q):
        w, x, y, z = q
        return (w, -x, -y, -z)

    def _qv_mult(self,q1, v1):
        q2 = [0.0,] + v1
        return self._q_mult(self._q_mult(q1, q2), self._q_conjugate(q1))[1:]

    def _q_mult(self,q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return w, x, y, z

    def _euler_to_quaternion(self,phi, theta, psi):
     
        qw = math.cos(phi/2) * math.cos(theta/2) * math.cos(psi/2) + math.sin(phi/2) * math.sin(theta/2) * math.sin(psi/2)
        qx = math.sin(phi/2) * math.cos(theta/2) * math.cos(psi/2) - math.cos(phi/2) * math.sin(theta/2) * math.sin(psi/2)
        qy = math.cos(phi/2) * math.sin(theta/2) * math.cos(psi/2) + math.sin(phi/2) * math.cos(theta/2) * math.sin(psi/2)
        qz = math.cos(phi/2) * math.cos(theta/2) * math.sin(psi/2) - math.sin(phi/2) * math.sin(theta/2) * math.cos(psi/2)
        
        return (qw, qx, qy, qz)

    def _quaternion_to_euler(self,w, x, y, z):
        # function has error,
        # _quaternion_to_euler(_euler_to_quaternion(phi, theta, psi)) != [phi, theta, psi]
        t0 = 2 * (w * x + y * z)
        t1 = 1 - 2 * (x * x + y * y)
        X = math.atan2(t0, t1)
     
        t2 = 2 * (w * y - z * x)
        t2 = 1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        Y = math.asin(t2)
             
        t3 = 2 * (w * z + x * y)
        t4 = 1 - 2 * (y * y + z * z)
        Z = math.atan2(t3, t4)
     
        return X, Y, Z
        
    def _normalize(self,v, tolerance=0.00001):
        mag2 = sum(n * n for n in v)
        if abs(mag2 - 1.0) > tolerance:
            mag = math.sqrt(mag2)
            v = tuple(n / mag for n in v)
        return v

    def Rotate(self,phi,theta,psi):
        # rotate object
        # phi rotate degrees axis to right (z-axis)
        # theta rotate degrees axis going up (y-axis)
        # psi rotate degrees axis left-down (x-axis)
    
        phi = math.radians(phi)     # rotate axis to right (z-axis)
        theta = math.radians(theta) # rotate axis going up (y-axis)
        psi = math.radians(psi)     # rotate axis left-down (x-axis)
        q = self._euler_to_quaternion(phi, theta, psi)
        self.quaternion = self._q_mult(q,self.quaternion)     # or should it be reverse ?

    def Point(self,point):
        # translate point to transformed coordinates
        point = self._qv_mult(self.quaternion,point)
        return point[0] + self.originX, point[1] + self.originY, point[2] + self.originZ
    
    def List(self,array):
        # translate point to transformed coordinates
        ret = []
        for point in array:
            ret.append(self.Point(point))
        return ret

        
    
