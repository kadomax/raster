import math 

# vectors are treated as row vectors
class vec3:
    def __init__(self , x , y , z , w = 0): # be default w = 0 for a vector
        self.x = x
        self.y = y
        self.z = z
        self.w = w # homogeneous coordinate

    def __add__(self , v):
        return vec3(self.x + v.x , self.y + v.y , self.z + v.z)
    
    def __sub__(self , v):
        return vec3(self.x - v.x , self.y - v.y , self.z - v.z)
    
    def __xor__(self , v): # dot product
        return self.x * v.x + self.y * v.y + self.z * v.z
    
    def __mod__(self , v): # cross product
        return vec3(self.y*v.z - self.z*v.y , self.z*v.x - self.x*v.z , self.x*v.y - self.y*v.x)
    
    def __mul__(self , k): # scalar multiplication
        return vec3(self.x * k , self.y * k , self.z * k)
    
    def __rmul__(self, k): # scalar multiplication
        return vec3(self.x * k , self.y * k , self.z * k)
    
    def __eq__(self , v):
        if self.x == v.x and self.y == v.y and self.z == v.z:
            return True
        return False
    
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self):
        return vec3(self.x / self.norm() , self.y / self.norm() , self.z / self.norm())
    

    def print_vec(self):
        print("<%f %f %f>"%(self.x , self.y , self.z))


class vec2:
    def __init__(self , x , y):
        self.x = x
        self.y = y

    def __add__(self , v):
        return vec2(self.x + v.x , self.y + v.y)
    
    def __sub__(self , v):
        return vec2(self.x - v.x , self.y - v.y)
    
    def __xor__(self , v): # dot product
        return self.x * v.x + self.y * v.y
    
    def __mod__(self , v): # cross product
        return self.x*v.y - self.y*v.x
    
    def __mul__(self , k): # scalar multiplication
        return vec2(self.x * k , self.y * k)
    
    def __rmul__(self, k): # scalar multiplication
        return vec2(self.x * k , self.y * k)
    
    def __eq__(self , v):
        if self.x == v.x and self.y == v.y:
            return True
        return False
    
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        return vec3(self.x / self.norm() , self.y / self.norm())

    def print_vec(self):
        print("<%f %f>"%(self.x , self.y))


def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def load_verts(path):
    verts = []
    with open(path , 'r') as f:
        for line in f:
            if line[0] == 'v' and line[1] == ' ':
                t = line.split(' ')
                 #print(float(t[3][:-1]))
                temp = vec3(float(t[1]) , float(t[2]) , float(t[3][:-1]))
                verts.append(temp)
    return verts


def load_indices(path):
    indices = []
    with open(path , 'r') as f:
        for line in f:
            if line[0] == 'f' and line[1] == ' ':
                y = line.split(' ')
                z = []
                for t in y:
                    temp = t.split('/')
                    if is_int(temp[0]):
                        z.append(int(temp[0]) - 1)
                indices.append(z)
    return indices


def toscreen(ndc , screen_width , screen_height):
    s = vec2(0 , 0)
    s.x = round(((ndc.x + 1) * screen_width) / 2)
    s.y = round(((1 - ndc.y) * screen_height) / 2)
    return s


def tondc(scr , screen_width , screen_height):
    n = vec2(0 , 0)
    n.x = ((2*scr.x / screen_width) - 1)
    n.y = (1 - (2*scr.y) / screen_height)
    return n


def mat4_mul(m4 , n4):
    r4 = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            s = 0
            for k in range(4):
                s += m4[i][k] + n4[k][j]
            r4[i][j] = s
    return r4
            

def mat3_mul(m3 , n3):
    r3 = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s += m3[i][k] + n3[k][j]
            r3[i][j] = s
    return r3


def transform(m , v):
    r = vec3(0 , 0 , 0)
    if len(m[0]) == 4:
        r.x = m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z + m[0][3] * v.w
        r.y = m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z + m[1][3] * v.w
        r.z = m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z + m[2][3] * v.w
        r.w = m[3][0] * v.x + m[3][1] * v.y + m[3][2] * v.z + m[3][3] * v.w
    elif len(m[0]) == 3:
        r.x = m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z
        r.y = m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z
        r.z = m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z
    return r


def rotate(angle , vertex , axis): # axis can only be x, y or z
    angle = angle % 360
    angle_radians = math.radians(angle)
    c = math.cos(angle_radians)
    s = math.sin(angle_radians)
    r_x = [[1 , 0 , 0] , [0 , c , -s] , [0 , s , c]]
    r_y = [[c , 0 , s] , [0 , 1 , 0] , [-s , 0 , c]]
    r_z = [[c , -s , 0] , [s , c , 0] , [0 , 0 , 1]]
    if axis == 'x':
        r = transform(r_x , vertex)
    elif axis == 'y':
        r = transform(r_y , vertex)
    elif axis == 'z':
        r = transform(r_z , vertex)
    return r




CAM_DISTANCE = -5
def project(v3 , aspect_ratio = 1):
    v2 = vec2(0 , 0)
    v2.x = aspect_ratio * v3.x / (v3.z - CAM_DISTANCE) # squishing or stretching only on the x based on the aspect ratio
    v2.y = v3.y / (v3.z - CAM_DISTANCE)
    return v2

LIGHT_VECTOR = vec3(4 , 3 , -7)
def calc_light(v1 , v2 , v3):
    light = (((v3-v1) % (v2-v1)).normalize() ^ (v1 - LIGHT_VECTOR).normalize())
    return light
