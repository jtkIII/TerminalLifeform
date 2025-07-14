# filepath: /home/jtk/Dev/TerminalLifeform/src/entity.py
import uuid

from faker import Faker

from params import entity_params

fake = Faker(["it_IT", "en_US", "ja_JP"])


class Entity:
    """
    Represents an individual entity in the simulation.

    Attributes:
        id (str): Unique identifier for the entity.
        age (int): Current age of the entity (in simulation Epochs).
        health (float): Current health of the entity (0.0 to 100.0).
        energy (float): Current energy level of the entity (0.0 to 100.0).
        status (str): Current status (e.g., 'alive', 'dead', 'thriving', 'struggling').
        parameters (dict): Customizable parameters for this specific entity type.
                           Examples: 'max_age', 'metabolism_rate', 'resilience'.
    """

    def __init__(self, initial_parameters=None):
        """
        Initializes a new entity with default or provided parameters.

        Args:
            initial_parameters (dict, optional): A dictionary of custom parameters
                                                 for this entity. Defaults to None.
        """
        self.id = str(uuid.uuid4())[:8]  # Short unique ID
        self.name = fake.last_name_nonbinary()
        self.age = 0
        self.health = 100.0
        self.energy = 100.0
        self.status = "alive"

        # Default parameters for an entity type
        self.parameters = entity_params.copy()

        # Override default parameters with any provided initial_parameters
        if initial_parameters:
            self.parameters.update(initial_parameters)

        self.health = self.parameters["initial_health"]
        self.energy = self.parameters["initial_energy"]

    def is_alive(self):
        """Checks if the entity is currently alive."""
        return self.status != "dead"

    def update_status(self):
        """
        Updates the entity's status based on its current health and energy.
        """
        if self.health <= 0 or self.age >= self.parameters["max_age"]:
            self.status = "dead"
            self.health = 0.0  # Ensure health is 0 when dead
            self.energy = 0.0  # Ensure energy is 0 when dead
        elif (
            self.health >= self.parameters["thriving_threshold_health"]
            and self.energy >= self.parameters["thriving_threshold_energy"]
        ):
            self.status = "thriving"
        elif (
            self.health <= self.parameters["struggling_threshold_health"]
            or self.energy <= self.parameters["struggling_threshold_energy"]
        ):
            self.status = "struggling"
        else:
            self.status = "alive"  # Default status if not thriving, struggling, or dead

    def __repr__(self):
        """String representation of the entity."""
        return (
            f"Entity(ID:{self.id}, {self.name} Age:{self.age}, Health:{self.health:.1f}, "
            f"Energy:{self.energy:.1f}, Status:'{self.status}')"
        )
