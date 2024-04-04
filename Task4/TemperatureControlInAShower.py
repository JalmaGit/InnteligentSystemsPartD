from simpful import *

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
FS.set_variable("temp", 10)
FS.set_variable("flow", 1)

# Perform Mamdani inference and print output
print(FS.Mamdani_inference(["cold"]))
print(FS.Mamdani_inference(['hot']))


# Plot Surface Maps
figCold = FS.plot_surface(variables=['temp','flow'],output='cold')
figHot = FS.plot_surface(variables=['temp','flow'],output='hot')

# Plot Linquistic Variables
fig1 = FS.plot_variable(var_name='temp')
fig2 = FS.plot_variable(var_name='flow')
fig3 = FS.plot_variable(var_name='cold')
fig4 = FS.plot_variable(var_name='hot')