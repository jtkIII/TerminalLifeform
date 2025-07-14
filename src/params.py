# filepath: /home/jtk/Dev/TerminalLifeform/src/params.py
import random

entity_params = {
    "max_age": 101,
    "initial_health": 100.0,
    "initial_energy": 100.0,
    "metabolism_rate": 0.3,
    "health_recovery_rate": 1.3,
    "health_decay_rate": 1.5,
    "resilience": 0.21,
    "thriving_threshold_health": 65.0,
    "thriving_threshold_energy": 60.0,
    "struggling_threshold_health": 33.0,
    "struggling_threshold_energy": 22.0,
    "reproduction_chance": 1.58,
    "min_reproduction_age": 13,
    "aggression": 0.3,
    "cooperation": 0.1,
}

default_environment_factors = {
    "resource_availability": 1.0,  # 0.0 (scarce) to 1.0 (abundant)
    "temperature": 25.0,  # Temperature in Celsius
    "pollution": 0.0,  # 0.0 (clean) to 1.0 (polluted)
    "event_chance": 0.035,  # Chance of a random event per step
    "interaction_strength": 0.5,  # Base strength of entity interactions
    "mutation_rate": 0.13,  # Probability of a parameter mutating (0.0 to 1.0)
    "mutation_strength": 0.05,  # Max percentage change for a mutation (e.g., 0.05 = 5%)
    "predator_threshold": 15,  # Population threshold to trigger predator event
    "predator_impact_percentage": 0.2,  # Percentage of population removed by predator
}

# Override with specific simulation parameters
sim_env_params = {
    "temperature": 20.0,
    "pollution": 0.1,
    "event_chance": 0.08,
    "interaction_strength": 0.5,
    "mutation_rate": 0.3,
    "mutation_strength": 0.13,
    "predator_threshold": 25,
    "predator_impact_percentage": 0.2,
}

hardy_entity_params = {
    "max_age": 150,
    "resilience": 0.33,
    "metabolism_rate": 0.4,
    "reproduction_chance": 0.3,
    "aggression": 0.3,
}

random_parameters = {
    "max_age": random.randint(55, 111),
    "metabolism_rate": random.uniform(0.1, 1.0),
    "resilience": random.uniform(0.0, 1.0),
    "reproduction_chance": random.uniform(0.05, 0.3),
    "aggression": random.uniform(0.0, 1.0),
}

max_parameters = {
    "max_age": 200,
    "metabolism_rate": 1.0,
    "resilience": 1.0,
    "reproduction_chance": 0.5,
    "aggression": 1.0,
}
