import argparse
import math
import random

from collections import namedtuple

from enum import Enum

class Status(Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3

parser = argparse.ArgumentParser(description='Arguments for a simple SIR model.')
parser.add_argument('--population', default=1000000, type=int,
                    help='population size')
parser.add_argument('--initial_recovered', default=0, type=int,
                    help='recovered / immune population at start of simulation')
parser.add_argument('--initial_infected', default=1, type=int,
                    help='number of infected people at start of simulation')
parser.add_argument('--r0', default=2.5, type=float,
                    help='r0 for the disease')
args = parser.parse_args()

population = []
num_infected = args.initial_infected
num_recovered = args.initial_recovered
num_susceptible = args.population - num_infected - num_recovered

for i in range(num_recovered):
    population.append(Status.RECOVERED)
infected = set()
for i in range(num_infected):
    infected.add(len(population))
    population.append(Status.INFECTED)
for i in range(args.population - num_recovered - num_infected):
    population.append(Status.SUSCEPTIBLE)

r0_remainder = args.r0 % 1
r0_whole = math.floor(args.r0 - r0_remainder)

iteration = 0
print("At time 0, there are {} infected, {} recovered, and {} susceptible".format(num_infected, num_recovered, num_susceptible))
while num_infected > 0:
    iteration = iteration + 1
    newly_infected = set()
    for i in range(num_infected):
        # note that drawing like this is quite lazy - someone can possibly contact themselves
        if random.random() < r0_remainder:
            contacts = random.sample(range(len(population)), r0_whole + 1)
        else:
            contacts = random.sample(range(len(population)), r0_whole)
        for contact in contacts:
            if population[contact] is Status.SUSCEPTIBLE:
                newly_infected.add(contact)
    for recovered in infected:
        population[recovered] = Status.RECOVERED
    num_recovered = num_recovered + len(infected)
    infected = newly_infected
    for contact in infected:
        population[contact] = Status.INFECTED
    num_infected = len(infected)
    num_susceptible = len(population) - num_infected - num_recovered
    print("At time {}, there are {} infected, {} recovered, and {} susceptible".format(iteration, num_infected, num_recovered, num_susceptible))

