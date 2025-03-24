# genetic.py

import copy
import random
import torch
import numpy as np

from serf import BotNet, BOT_COUNT, INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS


class GeneticAlgorithm:
    def __init__(self,
                 population_size=6,
                 mutation_rate=0.01,
                 crossover_rate=0.5,
                 elitism=2,
                 device='cpu'):
        """
        Basic Genetic Algorithm to evolve multiple BotNet models.

        :param population_size: Number of models in the population
        :param mutation_rate: Probability of mutating each parameter
        :param crossover_rate: Probability of crossover between two parents
        :param elitism: Number of top models to carry over to next generation
        :param device: 'cpu' or 'cuda'
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.device = device

        # Initialize a population of BotNets
        self.population = [BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS).to(self.device)
                           for _ in range(population_size)]

        # Will hold fitness scores for each model in the population
        self.fitness_scores = [0.0] * population_size

    def evaluate_fitness(self, env):
        """
        Evaluate each model in the population using a custom fitness function.
        Typically, you'd run each model in the environment for some episodes
        and measure total reward, survival time, etc.

        :param env: Your environment to test the models
        """
        for i, model in enumerate(self.population):
            # Reset / initialize environment, run model, gather rewards
            # For demonstration, we just assign a random fitness.
            # Replace with your actual environment interaction.

            # Example (pseudo-code):
            # total_reward = 0
            # for episode in range(num_episodes):
            #     obs = env.reset()
            #     done = False
            #     while not done:
            #         action = self.forward_action(model, obs)
            #         next_obs, reward, done, info = env.step(action)
            #         total_reward += reward
            #         obs = next_obs
            # self.fitness_scores[i] = total_reward

            # Dummy random fitness for illustration:
            self.fitness_scores[i] = random.random() * 100

    def forward_action(self, model, obs):
        """
        Example method for getting an action from the model.
        Replace with your custom observation-to-action pipeline.
        """
        with torch.no_grad():
            obs_tensor = torch.tensor(obs, dtype=torch.float32).to(self.device)
            q_values = model(obs_tensor.unsqueeze(0))
            action = q_values.argmax(dim=1).item()
        return action

    def select_parents(self):
        """
        Select parents for crossover using a simple tournament or roulette wheel, etc.
        This example uses a simple 'roulette wheel' approach based on fitness.
        """
        total_fitness = sum(self.fitness_scores)
        if total_fitness == 0:
            # If all fitness are zero, pick randomly
            return random.choice(self.population)

        pick = random.uniform(0, total_fitness)
        current = 0
        for model, score in zip(self.population, self.fitness_scores):
            current += score
            if current > pick:
                return model
        return self.population[-1]

    def crossover(self, parent1, parent2):
        """
        Perform crossover of parameters from two parent models.
        We treat the flattened parameters as a 1D array and split them.
        """
        child1 = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS).to(self.device)
        child2 = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS).to(self.device)

        # Get parameter vectors
        parent1_params = self.get_params(parent1)
        parent2_params = self.get_params(parent2)

        # Single point crossover
        if random.random() < self.crossover_rate:
            cut_point = random.randint(1, len(parent1_params) - 1)
            child1_params = torch.cat((parent1_params[:cut_point],
                                       parent2_params[cut_point:]))
            child2_params = torch.cat((parent2_params[:cut_point],
                                       parent1_params[cut_point:]))
        else:
            child1_params = parent1_params
            child2_params = parent2_params

        # Load params back into children
        self.set_params(child1, child1_params)
        self.set_params(child2, child2_params)

        return child1, child2

    def mutate(self, model):
        """
        Mutate model parameters by adding small Gaussian noise.
        """
        params = self.get_params(model)
        for i in range(len(params)):
            if random.random() < self.mutation_rate:
                params[i] += torch.randn(1, device=self.device) * 0.1
        self.set_params(model, params)

    def get_params(self, model):
        """
        Flatten model parameters into a 1D tensor.
        """
        return torch.cat([p.view(-1) for p in model.parameters()])

    def set_params(self, model, flat_params):
        """
        Unflatten parameters back into model.
        """
        idx = 0
        for p in model.parameters():
            num_params = p.numel()
            p.data = flat_params[idx:idx + num_params].view(p.size())
            idx += num_params

    def evolve(self, env, generations=10):
        """
        Main GA loop: Evaluate, select, crossover, mutate.
        """
        for gen in range(generations):
            # 1) Evaluate fitness for the current population
            self.evaluate_fitness(env)

            # 2) Sort population by fitness
            sorted_indices = sorted(range(self.population_size),
                                    key=lambda i: self.fitness_scores[i],
                                    reverse=True)

            # 3) Elitism: carry over top N models
            new_population = [copy.deepcopy(self.population[idx]) for idx in sorted_indices[:self.elitism]]

            # 4) Fill the rest of the population
            while len(new_population) < self.population_size:
                parent1 = self.select_parents()
                parent2 = self.select_parents()
                child1, child2 = self.crossover(parent1, parent2)

                self.mutate(child1)
                self.mutate(child2)

                new_population.extend([child1, child2])

            # Update population with new generation
            self.population = new_population[:self.population_size]

            # For debugging/logging
            best_fitness = max(self.fitness_scores)
            avg_fitness = sum(self.fitness_scores) / self.population_size
            print(f"Generation {gen + 1}: Best Fitness = {best_fitness:.2f}, Avg Fitness = {avg_fitness:.2f}")

    def inject_dqn_models(self, dqn_models):
        """
        Optional: inject trained DQN models into GA population.

        :param dqn_models: list of DQN models (BotNet) you'd like to seed into the GA
        """
        # Replace the first few members of the GA population
        # with these DQN models (assuming same architecture).
        for i in range(min(len(dqn_models), self.population_size)):
            dqn_params = self.get_params(dqn_models[i])
            self.set_params(self.population[i], dqn_params)
        print("Injected DQN weights into GA population.")


