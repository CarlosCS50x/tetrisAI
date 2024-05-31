import random
from agent import Agent

def select_top_agents(agents, fitness_scores, num_top_agents=2):
    sorted_agents = sorted(zip(agents, fitness_scores), key=lambda x: x[1], reverse=True)
    return [agent for agent, score in sorted_agents[:num_top_agents]]

def generate_new_population(top_agents, population_size):
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = random.sample(top_agents, 2)
        child = parent1.crossover(parent2)
        child.mutate()
        new_population.append(child)
    return new_population