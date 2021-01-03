from cau5 import *
import csv
def rk4(dx, x0, y0, x, h): 
    # Count number of iterations using step size or 
    # step height h 
    n = (int)((x - x0)/h)  
    # Iterate for number of iterations 
    y = y0 
    for i in range(1, n + 1): 
        k1 = h * dx(x0, y) 
        k2 = h * dx(x0 + 0.5 * h, y + 0.5 * k1) 
        k3 = h * dx(x0 + 0.5 * h, y + 0.5 * k2) 
        k4 = h * dx(x0 + h, y + k3) 
        y = y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 
        x0 = x0 + h 
    return y 

# Function for euler formula 
def euler(dx, x_init, func_val, step, x_fini, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr): 
    print ("INIT VP_air " + str(func_val))
    print ("INIT VP_top " + str(VP_top))
    while x_init < x_fini: 
        (a,b) = dx(VP_air = func_val, T_air = T_air, VP_out = VP_out , T_out = T_out, T_top = T_top, VP_top = VP_top, T_thscr = T_thscr, U_roof = U_roof, U_thscr = U_thscr, VP_thscr = VP_thscr)
        func_val = func_val + step * a
        print("dx " +str(a) + "\t" + str(b))
        VP_top = VP_top + step*b
        x_init = x_init + step
        print("VP_top " + str(VP_top))
        print("VP_air " + str(func_val))
        print("END\n")
    return func_val
   
def cal_saturation_pressure(t):
    return 610.78 * exp( t / ( t + 238.3 ) * 17.2694)
    
def cal_VP(rhAir, t):
    return rhAir * cal_saturation_pressure(t) / 100.0
      
data = []
with open("Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        data.append(row)
VP_air = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))
VP_top = VP_air
VP_air_compare = VP_air
VP_out = VP_air
solver = Solver()
#print(VP_air)
Vp_air_compare = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))    #extract VP_air value from the dataset
#print(VP_air_compare)

T_air = float(data[0]["Tair"])  #air temperature
T_out = T_air + 1               #temperature of the air outside
T_thscr = T_air + 1             #temperature of the thermal screen
T_top = T_air                   #temperature in the top room
VP_top = VP_air
VP_thscr = cal_saturation_pressure(T_thscr)
U_roof = (float(data[0]["VentLee"]) + float(data[0]["Ventwind"])) / 200.0
U_thscr = float(data[0]["EnScr"]) / 100

d = solver.dx(VP_air = VP_air, T_air = T_air, VP_out = VP_out, T_out = T_out, T_top = T_top, T_thscr = T_thscr, U_roof = U_roof, U_thscr = U_thscr, VP_top = VP_top, VP_thscr = VP_thscr)[0]
VP_air = euler(solver.dx, 0, VP_air, 2.5, 5, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr)
print("%f %f" %(cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"])), VP_air))
