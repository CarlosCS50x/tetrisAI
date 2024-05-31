from agent import Agent
from evolution import select_top_agents, generate_new_population
from tetris import TetrisAI

# Initialize population
population_size = 5
agents = [Agent() for _ in range(population_size)]

num_generations = 100
for generation in range(num_generations):
    fitness_scores = []
    for agent in agents:
        game = TetrisAI(agent)
        score = game.run()
        fitness_scores.append(score)
    
    top_agents = select_top_agents(agents, fitness_scores)
    agents = generate_new_population(top_agents, population_size)
    print(f"Generation {generation} complete")

print("Training complete")