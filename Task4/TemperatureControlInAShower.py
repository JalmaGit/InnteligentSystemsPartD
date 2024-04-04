from simpful import *
import simupy as sp
import Shower as SH
import time
import matplotlib.pyplot as plt

# Temprature Control in a Shower problem
# Create a fuzzy system object
FS = FuzzySystem()

# Define fuzzy sets and linguistic variables
S_1 = FuzzySet(function=Trapezoidal_MF(a=-20, b=-20, c=-15, d=0), term="cold")
S_2 = FuzzySet(function=Triangular_MF(a=-10, b=0, c=10), term="good")
S_3 = FuzzySet(function=Trapezoidal_MF(a=0, b=15, c=20, d=20), term="hot")
FS.add_linguistic_variable("temp", LinguisticVariable([S_1, S_2, S_3], concept="Water Temperature", universe_of_discourse=[-20,20]))

F_1 = FuzzySet(function=Trapezoidal_MF(a=-1, b=-1, c=-0.8, d=0), term="soft")
F_2 = FuzzySet(function=Triangular_MF(a=-0.4, b=0, c=0.4), term="good")
F_3 = FuzzySet(function=Trapezoidal_MF(a=0, b=0.8, c=1, d=1), term="hard")
FS.add_linguistic_variable("flow", LinguisticVariable([F_1, F_2, F_3], concept="Water Flow", universe_of_discourse=[-1,1]))

# Define output fuzzy sets and linguistic variable
C_1 = FuzzySet(function=Triangular_MF(a=-1, b=-0.6, c=-0.3), term="closeFast")
C_2 = FuzzySet(function=Triangular_MF(a=-0.6, b=-0.3, c=0), term="closeSlow")
C_3 = FuzzySet(function=Triangular_MF(a=-0.3, b=0, c=0.3), term="steady")
C_4 = FuzzySet(function=Triangular_MF(a=0, b=0.3, c=0.6), term="openSlow")
C_5 = FuzzySet(function=Triangular_MF(a=0.3, b=0.6, c=1), term="openFast")
FS.add_linguistic_variable("cold", LinguisticVariable([C_1, C_2, C_3, C_4, C_5], universe_of_discourse=[-1,1]))

H_1 = FuzzySet(function=Triangular_MF(a=-1, b=-0.6, c=-0.3), term="closeFast")
H_2 = FuzzySet(function=Triangular_MF(a=-0.6, b=-0.3, c=0), term="closeSlow")
H_3 = FuzzySet(function=Triangular_MF(a=-0.3, b=0, c=0.3), term="steady")
H_4 = FuzzySet(function=Triangular_MF(a=0, b=0.3, c=0.6), term="openSlow")
H_5 = FuzzySet(function=Triangular_MF(a=0.3, b=0.6, c=1), term="openFast")
FS.add_linguistic_variable("hot", LinguisticVariable([H_1, H_2, H_3, H_4, H_5], universe_of_discourse=[-1,1]))

# Define fuzzy rules
R1 = "IF (temp IS cold) AND (flow IS soft) THEN (cold IS openSlow)"
R2 = "IF (temp IS cold) AND (flow IS good) THEN (cold IS closeSLow)"
R3 = "IF (temp IS cold) AND (flow IS hard) THEN (cold IS closeFast)"
R4 = "IF (temp IS good) AND (flow IS soft) THEN (cold IS openSlow)"
R5 = "IF (temp IS good) AND (flow IS good) THEN (cold IS steady)"
R6 = "IF (temp IS good) AND (flow IS hard) THEN (cold IS closeSlow)"
R7 = "IF (temp IS hot) AND (flow IS soft) THEN (cold IS openFast)"
R8 = "IF (temp IS hot) AND (flow IS good) THEN (cold IS openSlow)"
R9 = "IF (temp IS hot) AND (flow IS hard) THEN (cold IS closeSlow)"
R10 = "IF (temp IS cold) AND (flow IS soft) THEN (hot IS openFast)"
R11 = "IF (temp IS cold) AND (flow IS good) THEN (hot IS openSlow)"
R12 = "IF (temp IS cold) AND (flow IS hard) THEN (hot IS closeSlow)"
R13 = "IF (temp IS good) AND (flow IS soft) THEN (hot IS openSlow)"
R14 = "IF (temp IS good) AND (flow IS good) THEN (hot IS steady)"
R15 = "IF (temp IS good) AND (flow IS hard) THEN (hot IS closeSlow)"
R16 = "IF (temp IS hot) AND (flow IS soft) THEN (hot IS openSlow)"
R17 = "IF (temp IS hot) AND (flow IS good) THEN (hot IS closeSlow)"
R18 = "IF (temp IS hot) AND (flow IS hard) THEN (hot IS closeFast)"
FS.add_rules([R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18])

# Set antecedents values
#FS.set_variable("temp", 10)
#FS.set_variable("flow", 1)

# Perform Mamdani inference and print output
#print(FS.Mamdani_inference(["cold"])['cold'])
#print(FS.Mamdani_inference(['hot']))

def ploting ():
    # Plot Surface Maps
    figCold = FS.plot_surface(variables=['temp','flow'],output='cold')
    figHot = FS.plot_surface(variables=['temp','flow'],output='hot')

    # Plot Linquistic Variables
    fig1 = FS.plot_variable(var_name='temp')
    fig2 = FS.plot_variable(var_name='flow')
    fig3 = FS.plot_variable(var_name='cold')
    fig4 = FS.plot_variable(var_name='hot')


# Initilize System
Shower = SH.Shower()
start_temp = 20
start_flow = 0.5
FS.set_variable("temp", 0)
FS.set_variable("flow", 0)
start_time = time.time()
last_time = time.time()
run_time = 0
dt = 0

# Initilizer Logger
time_logg = []
set_point_temp_logg = []
set_point_flow_logg = []
temp_logg = []
flow_rate_logg = []

while True:
    dt = time.time() - last_time
    last_time = time.time()

    #Step Input
    if 3 <= run_time:
        Shower.temp_set_point = 23
        Shower.flow_set_point = 1
    else:
        Shower.temp_set_point = start_temp
        Shower.flow_set_point = start_flow

    # Perform Mamdani inference
    cold = FS.Mamdani_inference(['cold'])['cold']
    hot = FS.Mamdani_inference(['hot'])['hot']

    # Turn Shower Valves
    flow_cold, temp_cold = Shower.cold_water_valve(cold, dt, run_time)
    flow_hot, temp_hot = Shower.hot_water_valve(hot, dt, run_time)

    temp_error, temp = Shower.temp_error(flow_hot,temp_hot, flow_cold, temp_cold, run_time)
    flow_error, flow_rate = Shower.flow_error(flow_hot,flow_cold, run_time)

    # Set antecedents values
    FS.set_variable("temp",temp_error)
    FS.set_variable("flow",flow_error)

    #print(f"Debugger: {cold=}, {hot=}, {temp_error=}, {flow_error=}")

    # Logger
    time_logg.append(run_time)
    set_point_temp_logg.append(Shower.temp_set_point)
    set_point_flow_logg.append(Shower.flow_set_point)
    temp_logg.append(temp)
    flow_rate_logg.append(flow_rate)


    run_time = time.time() - start_time

    if run_time > 6:
        break


# Plotter
fig, ax = plt.subplots()
ax.plot(time_logg,set_point_temp_logg, '-b', label='Step Input')
ax.plot(time_logg,temp_logg, '-r', label='System Response')
ax.grid(True)
fig.show()
plt.show()
print("Success")
    