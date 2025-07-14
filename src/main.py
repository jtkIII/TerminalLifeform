import random
import time

from colored import Back, Fore, Style
from tqdm import tqdm

from entity import Entity
from entity_utils import calculate_energy_change, calculate_health_change
from logging_config import setup_logger
from params import (
    default_environment_factors,
    hardy_entity_params,
    max_parameters,
    random_parameters,
    sim_env_params,
)

logger = setup_logger(__name__)


class Simulation:
    """
    Manages the overall simulation, including entities, time, and environment.
    """

    def __init__(self, initial_entities=5, time_steps=1000, environment_params=None):
        self.entities = []
        self.current_time = 0
        self.total_time_steps = time_steps
        """
        Initializes the simulation.

        Args:
            initial_entities (int): Number of entities to start with.
            time_steps (int): Total number of Epochs to run the simulation.
            environment_params (dict, optional): Initial environmental factors.
        """
        self.entities = []
        self.current_time = 0
        self.total_time_steps = time_steps

        # Use imported default_environment_factors
        self.environment_factors = default_environment_factors.copy()
        if environment_params:
            self.environment_factors.update(environment_params)

        # Populate initial entities
        for _ in range(initial_entities):
            self.add_entity(Entity())

        logger.info(f"Simulation initialized with {len(self.entities)} entities.")

    def add_entity(self, entity):
        """Adds a new entity to the simulation."""
        self.entities.append(entity)
        logger.info(f"Added new entity: {entity.id}")

    def _update_environment(self):
        """
        Updates environmental factors over time or based on random events.
        This is a simple example; could be much more complex.
        """

        # Gradual changes over time
        self.environment_factors["resource_availability"] = max(
            0.1, 1.0 - (self.current_time / self.total_time_steps) * 0.5
        )

        self.environment_factors["temperature"] = 25.0 + 10 * (
            self.current_time / self.total_time_steps - 0.5
        )  # Oscillates

        self.environment_factors["pollution"] = min(
            0.8, (self.current_time / self.total_time_steps) * 0.3
        )

        # Random events
        if random.random() < self.environment_factors["event_chance"]:
            event_type = random.choice(
                ["resource_spike", "disease_outbreak", "heatwave"]
            )
            if event_type == "resource_spike":
                self.environment_factors["resource_availability"] = min(
                    1.0, self.environment_factors["resource_availability"] + 0.2
                )
                logger.info(
                    f"Time {self.current_time}: {Back.yellow}Environmental Event - Resource Spike!{Style.reset}"
                )
            elif event_type == "disease_outbreak":
                # Reduce health of a random subset of entities
                for entity in random.sample(self.entities, min(len(self.entities), 3)):
                    if entity.is_alive():
                        entity.health = max(0, entity.health - random.uniform(10, 30))
                logger.info(
                    f"Time {self.current_time}: {Back.red} Environmental Event - Disease Outbreak! {Style.reset}"
                )
            elif event_type == "heatwave":
                self.environment_factors["temperature"] = min(
                    45.0,
                    self.environment_factors["temperature"] + random.uniform(5, 10),
                )
                logger.info(
                    f"Time {self.current_time}: {Back.red} Environmental Event - Heatwave! {Style.reset}"
                )

        # Dynamic Event: Predator if population is too high
        alive_count = len([e for e in self.entities if e.is_alive()])
        if alive_count > self.environment_factors["predator_threshold"]:
            num_to_remove = int(
                alive_count * self.environment_factors["predator_impact_percentage"]
            )
            num_to_remove = max(
                1, num_to_remove
            )  # Ensure at least one entity is removed if threshold is met

            # Select entities to be removed/damaged by predator
            # Prioritize struggling entities if possible, otherwise random
            struggling_entities = [
                e for e in self.entities if e.status == "struggling" and e.is_alive()
            ]
            if len(struggling_entities) >= num_to_remove:
                targets = random.sample(struggling_entities, num_to_remove)
            else:
                targets = random.sample(
                    [e for e in self.entities if e.is_alive()],
                    min(num_to_remove, alive_count),
                )

            for entity in targets:
                entity.health = 0  # Predator instantly kills
                entity.update_status()  # Mark as dead
                logger.info(
                    f"{Style.BOLD}{Fore.cyan} Time {self.current_time}: Dynamic Event - Predator! Entity {entity.id} was removed.{Style.reset}"
                )

    def _process_entity(self, entity):
        """
        Applies all updates to a single entity for the current Epoch.
        """
        if not entity.is_alive():
            return  # Skip dead entities

        entity.age += 1

        energy_change = calculate_energy_change(entity, self.environment_factors)
        entity.energy = max(0.0, min(100.0, entity.energy + energy_change))

        health_change = calculate_health_change(entity, self.environment_factors)
        entity.health = max(0.0, min(100.0, entity.health + health_change))

        entity.update_status()

    def _handle_interactions(self):
        """
        Handles interactions between entities, e.g., resource competition.
        """
        alive_entities = [e for e in self.entities if e.is_alive()]
        num_alive = len(alive_entities)

        if num_alive < 2:
            return  # No interactions if less than 2 entities

        # Interaction intensity increases with population density and low resources
        interaction_modifier = (
            1.0 - self.environment_factors["resource_availability"]
        ) + (num_alive / 100.0)  # Simple scaling
        interaction_modifier = min(
            1.0, max(0.1, interaction_modifier)
        )  # Clamp between 0.1 and 1.0

        for _, entity1 in enumerate(alive_entities):
            # Each entity interacts with a small random subset of others
            # To avoid N*N complexity for large populations
            num_interactions = min(
                num_alive - 1, 3
            )  # Interact with up to 3 other entities
            potential_targets = [e for e in alive_entities if e.id != entity1.id]

            if not potential_targets:
                continue

            for entity2 in random.sample(potential_targets, num_interactions):
                # Simple competition: entities lose health/energy based on aggression and resource scarcity
                if entity1.is_alive() and entity2.is_alive():
                    # Entity1 impacts Entity2
                    damage_to_entity2 = (
                        entity1.parameters["aggression"]
                        * self.environment_factors["interaction_strength"]
                        * interaction_modifier
                    )
                    entity2.health = max(0.0, entity2.health - damage_to_entity2)
                    entity2.energy = max(
                        0.0, entity2.energy - damage_to_entity2 / 2
                    )  # Energy loss is half of health loss

                    # Entity2 impacts Entity1 (can be symmetrical or asymmetrical)
                    damage_to_entity1 = (
                        entity2.parameters["aggression"]
                        * self.environment_factors["interaction_strength"]
                        * interaction_modifier
                    )
                    entity1.health = max(0.0, entity1.health - damage_to_entity1)
                    entity1.energy = max(0.0, entity1.energy - damage_to_entity1 / 2)

                    logger.debug(
                        f"Time {self.current_time}: Interaction between {entity1.id} and {entity2.id}. "
                        f"E1 Health:{entity1.health:.1f}, E2 Health:{entity2.health:.1f}"
                    )
                    # Note: Using debug level for frequent interaction logs to avoid overwhelming INFO level output

    def _apply_mutation(self, params):
        """
        Applies slight random mutations to entity parameters.
        Args:
            params (dict): The dictionary of parameters to mutate.
        Returns:
            dict: The mutated parameters.
        """
        mutated_params = params.copy()
        mutation_rate = self.environment_factors["mutation_rate"]
        mutation_strength = self.environment_factors["mutation_strength"]

        # Parameters that can mutate and their bounds/types
        mutable_parameters = {
            "max_age": {"min": 50, "max": 200, "type": int},
            "metabolism_rate": {"min": 0.1, "max": 1.0, "type": float},
            "resilience": {"min": 0.0, "max": 1.0, "type": float},
            "reproduction_chance": {"min": 0.01, "max": 0.15, "type": float},
            "aggression": {"min": 0.0, "max": 1.0, "type": float},
        }

        for param_name, config in mutable_parameters.items():
            if random.random() < mutation_rate:
                original_value = mutated_params[param_name]
                change = original_value * random.uniform(
                    -mutation_strength, mutation_strength
                )

                if config["type"] is int:
                    new_value = int(round(original_value + change))
                else:  # float
                    new_value = original_value + change

                # Apply bounds
                new_value = max(config["min"], min(config["max"], new_value))

                mutated_params[param_name] = new_value
                logger.info(
                    f" {Fore.magenta} {Style.BOLD} Mutation: Parameter '{param_name}' changed from {original_value:.2f} to {new_value:.2f}{Style.reset}"
                )

        return mutated_params

    def _handle_reproduction(self):
        """
        Checks for thriving entities and potentially adds new offspring.
        """
        new_entities = []
        for entity in self.entities:
            if (
                entity.status == "thriving"
                and entity.age >= entity.parameters["min_reproduction_age"]
                and random.random() < entity.parameters["reproduction_chance"]
            ):
                # Create a new entity with parameters from parent
                offspring_params = entity.parameters.copy()

                # Apply mutations to offspring parameters
                offspring_params = self._apply_mutation(offspring_params)

                # Initial health/energy can still have some randomness
                offspring_params["initial_health"] = random.uniform(80, 100)
                offspring_params["initial_energy"] = random.uniform(80, 100)

                new_entity = Entity(offspring_params)
                new_entities.append(new_entity)
                logger.info(
                    f" {Back.red}Time {self.current_time}: Entity {entity.id} reproduced! New entity {new_entity.id} born.{Style.reset}"
                )
        self.entities.extend(new_entities)

    def run_simulation(self):
        """
        Runs the simulation for the specified number of Epochs.
        """
        logger.info("\n--- Starting Simm ---")

        for t in tqdm(range(self.total_time_steps), desc="Simm Progress"):
            # Update current Epoch
            self.current_time = t
            logger.info(f"\n--- Epoch {self.current_time} ---")
            time.sleep(0.11)  # Simulate time passing
            # Update global environment factors
            self._update_environment()
            logger.info(
                f" {Fore.blue}Environment:{Style.reset} {Fore.green}Resources:{self.environment_factors['resource_availability']:.2f},  "
                f"Temp:{self.environment_factors['temperature']:.1f}C, Pollution:{self.environment_factors['pollution']:.2f} {Style.reset}"
            )

            # Process each entity individually
            for entity in self.entities:
                self._process_entity(entity)

            # Handle interactions between entities
            self._handle_interactions()

            # After all processing and interactions, update status and log
            for entity in self.entities:
                entity.update_status()  # Re-update status after interactions
                if entity.is_alive():
                    logger.info(f"{entity}")
                else:
                    logger.info(
                        f"{Back.yellow} {entity.id} died. (Age:{entity.age}) {Style.reset} "
                    )

            # Remove dead entities
            self.entities = [entity for entity in self.entities if entity.is_alive()]

            # Handle reproduction
            self._handle_reproduction()

            # Report current population
            alive_count = len(self.entities)
            thriving_count = sum(1 for e in self.entities if e.status == "thriving")
            struggling_count = sum(1 for e in self.entities if e.status == "struggling")

            logger.info(
                f" {Back.magenta} Population: Alive={alive_count}, Thriving={thriving_count}, Struggling={struggling_count}{Style.reset}"
            )

            if alive_count == 0:
                logger.info(
                    f"{Back.magenta}All entities have died. Simulation ending early.{Style.reset}"
                )
                break

        logger.info(f"\n--- Simulation Finished at Epoch {self.current_time} ---")
        logger.info(f"Final Population: {len(self.entities)} entities remaining.")
        for entity in self.entities:
            logger.info(f"  {entity}")


if __name__ == "__main__":
    my_simulation = Simulation(
        initial_entities=150,
        time_steps=250,
        environment_params=sim_env_params,
    )

    # Add a couple of 'hardy' entities to the mix
    my_simulation.add_entity(Entity(hardy_entity_params))
    my_simulation.add_entity(Entity(hardy_entity_params))
    my_simulation.add_entity(Entity(random_parameters))
    my_simulation.add_entity(Entity(random_parameters))
    my_simulation.add_entity(Entity(max_parameters))
    my_simulation.add_entity(Entity(max_parameters))

    # Run the simulation
    my_simulation.run_simulation()
