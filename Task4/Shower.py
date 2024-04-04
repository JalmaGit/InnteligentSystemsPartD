import numpy as np
from scipy import signal

class Shower:

    def __init__(self):
        self.last_hot_integrate = 0
        self.last_cold_integrate = 0
        self.temp_set_point = 20
        self.flow_set_point = 0.5

    def hot_water_valve(self, hot, dt, t):
        #Integrator
        integrator = np.clip((self.last_hot_integrate + (hot * dt)),0.15,2)
        self.last_hot_integrate = integrator

        print(f"{self.last_hot_integrate=}")

        #Max Flow
        max_flow_constant = 1
        signal_generator = 0 * np.sin(0.3 * t)
        max_flow = max_flow_constant + signal_generator

        #Flow_rate
        flow_rate_hot = integrator * (integrator <= max_flow) + max_flow * (integrator > max_flow)

        #Temp
        temp_hot = 30

        return flow_rate_hot, temp_hot

    def cold_water_valve(self, cold, dt, t):
        #Integrator
        integrator = np.clip((self.last_hot_integrate + (cold * dt)),0.15,2)
        self.last_hot_integrate = integrator

        #Max Flow
        max_flow_constant = 1
        signal_generator = 0 * np.sin(0.3 * t)
        max_flow = max_flow_constant + signal_generator

        #Flow_rate
        flow_rate_cold = integrator * (integrator <= max_flow) + max_flow * (integrator > max_flow)

        #Temp
        temp_cold = 10
        
        return flow_rate_cold, temp_cold

    def temp_error(self, hot_water_flow, temp_hot, cold_water_flow, temp_cold, t):
        
        #temp_variation = 4 * signal.square(0.214320 * t)
        temp_set_point_adder = self.flow_set_point #+ temp_variation
        temp = ((temp_hot * hot_water_flow + temp_cold * cold_water_flow)/(cold_water_flow + hot_water_flow))

        error =  temp - temp_set_point_adder

        return error, temp

    def flow_error(self, hot_water_flow, cold_water_flow, t):
        
        #flow_variation = 0.2 * signal.square(0.3 * t)
        flow_set_point_adder = self.flow_set_point #+ flow_variation
        flow_rate = (hot_water_flow + cold_water_flow)

        error = flow_rate - flow_set_point_adder

        return error, flow_rate