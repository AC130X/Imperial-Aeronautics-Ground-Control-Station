#TwoMotorControlsurf tailsitter in python
import matplotlib.pyplot as plt
import numpy as np

maxthrust = 5
mtow = 0.5
dt = 0.01
gravity = -9.81
time = 0


class Drone:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Z = 0

        self.L = 0
        self.M = 0
        self.N = 0

        self.U = 0 #m/s
        self.V = 0 #m/s
        self.W = 0 #m/s

        self.p = 0 #deg/s 
        self.q = 0 #deg/s
        self.r = 0 #deg/s

        self.theta = 90 #deg
        self.phi = 0 #deg
        self.psi = 0 #deg

        self.x = 0
        self.y = 0
        self.z = 0

        self.ThrustLeft = 0 #N
        self.ThrustRight = 0 #N
        self.DeflectionLeft = 0
        self.DeflectionRight = 0
        
        self.throttle = 0   
        self.deflection = 0

        self.prevZ = 0
        self.prevW = 0
        self.prevX = 0
        self.prevU = 0
        self.prevY = 0
        self.prevV = 0

        self.integralZVTOL = 0
        self.preverrorZVTOL = 0
        self.integralXVTOL = 0
        self.preverrorXVTOL = 0
        self.integralYVTOL = 0
        self.preverrorYVTOL = 0

    def translateZ(self,setpoint,current):
        error = setpoint - current
        Kp = 2.5
        Ki = 1
        Kd = 1
        self.integralZVTOL += error 
        
        P = Kp * error
        I = Ki * self.integralZVTOL * dt
        D = Kd * (error - self.preverrorZVTOL) / dt
        self.throttle = np.clip(P + I + D,0,1)
        self.preverrorZVTOL = error

    def translateX(self,setpoint,current):
        error = setpoint - current
        Kp = 2
        Ki = 0.1
        Kd = 5
        self.integralXVTOL += error 
        
        P = Kp * error
        I = Ki * self.integralXVTOL * dt
        D = Kd * (error - self.preverrorXVTOL) / dt
        self.deflection = np.clip(P + I + D,-15,15)*(np.pi/180)
        self.preverrorXVTOL = error
    
    def translateY(self,setpoint,current):
        error = setpoint - current
        Kp = 2
        Ki = 0.1
        Kd = 5
        self.integralYVTOL += error 
        
        P = Kp * error
        I = Ki * self.integralYVTOL * dt
        D = Kd * (error - self.preverrorYVTOL) / dt
        self.deflection = np.clip(P + I + D,-15,15)*(np.pi/180)
        self.preverrorYVTOL = error

    def update(self):
        #evaluating the z forces
        self.Z = (mtow * gravity) + (2 * maxthrust * self.throttle)*np.cos(self.deflection)   
        self.W += self.prevZ/mtow * dt
        self.z += self.prevW*dt + self.prevZ/mtow*(dt**2)/2       
        self.prevW = self.W
        self.prevZ = self.Z 

        #evalulating the x forces
        self.X =  (2 * maxthrust * self.throttle)*np.sin(self.deflection)   
        self.U += self.prevX/mtow * dt
        self.x += self.prevU*dt + self.prevX/mtow*(dt**2)/2       
        self.prevU = self.U
        self.prevX = self.X 

        


plt.ion()
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'b-o', markersize=4)
ax.set_xlim(0, 50)
ax.set_ylim(-10, 10)
ax.set_title("Height tracking with PID")

Tailsitter = Drone()

# 3. Start the while loop
while time<50:
    x_data.append(Tailsitter.x)
    y_data.append(Tailsitter.z)
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    Tailsitter.translateX(5,Tailsitter.x)
    Tailsitter.translateZ(5,Tailsitter.z)
    Tailsitter.update()
    time += dt
    plt.pause(0.01)


# 5. Turn off interactive mode and keep the final plot open
plt.ioff()
plt.show()