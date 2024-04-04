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
        integrator = np.clip((self.last_hot_integrate + (hot * dt)),0.0015,2)
        self.last_hot_integrate = integrator

        #Max Flow
        max_flow_constant = 1
        signal_generator = 0 * np.sin(0.3 * t)
        max_flow = max_flow_constant

        #Flow_rate
        flow_rate_hot = integrator * (integrator <= max_flow) + max_flow * (integrator > max_flow)

        #Temp
        temp_hot = 30

        #print(f"debugger: {integrator=}")

        return flow_rate_hot, temp_hot

    def cold_water_valve(self, cold, dt, t):
        #Integrator
        integrator = np.clip((self.last_cold_integrate + (cold * dt)),0.0015,2)
        self.last_cold_integrate = integrator

        #Max Flow
        max_flow_constant = 1
        signal_generator = 0 * np.sin(0.3 * t)
        max_flow = max_flow_constant

        #Flow_rate
        flow_rate_cold = integrator * (integrator <= max_flow) + max_flow * (integrator > max_flow)

        #Temp
        temp_cold = 10
        
        return flow_rate_cold, temp_cold

    def temp_error(self, flow_rate_hot, temp_hot, flow_rate_cold, temp_cold, t):
        
        temp_variation = 0.1 * signal.square(0.214320 * t)
        temp_set_point = self.temp_set_point  + temp_variation
        temp = (flow_rate_hot * temp_hot + flow_rate_cold * temp_cold)/(flow_rate_hot + flow_rate_cold)

        error =  temp - temp_set_point

        print(f"Debugging {temp=}, {temp_set_point=}, {error=}")

        return error, temp

    def flow_error(self, flow_rate_hot, flow_rate_cold, t):
        
        flow_variation = 0.2 * signal.square(0.3 * t)
        flow_set_point = self.flow_set_point + flow_variation
        flow_rate = flow_rate_hot + flow_rate_cold

        error = flow_rate - flow_set_point

        #print(f"Debugging {flow_rate=}, {flow_set_point=}, {error=}")

        return error, flow_rate