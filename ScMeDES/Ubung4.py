import simpy
import numpy as np
class MM1Queue:
    def __init__(self, env, arrival_rate, service_rate, initial_queue_length):
            self.env = env
            self.server = simpy.Resource(env, capacity=1)
            self.arrival_rate = arrival_rate
            self.service_rate = service_rate
            self.queue = initial_queue_length
            self.total_queue_length = 0
            self.total_waiting_time = 0
            self.num_departures = 0


    def arrival_process(self):
        while True:
            inter_arrival_time = np.random.exponential(1 / self.arrival_rate)
            yield self.env.timeout(inter_arrival_time)
            self.queue += 1
            self.total_queue_length += self.queue
            print(f"Arrival at {self.env.now:.2f}. Queue length: {self.queue}")

    def service_process(self):
        while True:
            with self.server.request() as req:
                yield req
                service_time = np.random.exponential(1 / self.service_rate)
                yield self.env.timeout(service_time)
                self.queue -= 1
                self.total_waiting_time += self.queue
                self.num_departures += 1
                print(f"Departure at {self.env.now:.2f}. Queue length: {self.queue}")

def simulate_mm1_queue(arrival_rate, service_rate, initial_queue_length, sim_time):
    env = simpy.Environment()
    mm1_queue = MM1Queue(env, arrival_rate, service_rate, initial_queue_length)

    env.process(mm1_queue.arrival_process())
    env.process(mm1_queue.service_process())

    env.run(until=sim_time)

    average_queue_length = mm1_queue.total_queue_length / sim_time
    average_waiting_time = mm1_queue.total_waiting_time / mm1_queue.num_departures
    lambda_ratio = average_queue_length / average_waiting_time

    return lambda_ratio

# Parameters
arrival_rate = 0.5  # λ = 0.5Hz
service_rate = 0.5  # μ = 0.5Hz
initial_queue_length = 5
simulation_time = 200

lambda_ratio = simulate_mm1_queue(arrival_rate, service_rate, initial_queue_length, simulation_time)
print(f"lambda_ratio: {lambda_ratio}")



