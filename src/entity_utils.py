def calculate_energy_change(entity, environment_factors):
    """
    Calculates the change in an entity's energy based on its metabolism
    and environmental factors (e.g., resource availability).

    Args:
        entity (Entity): The entity whose energy is being calculated.
        environment_factors (dict): Current environmental conditions.

    Returns:
        float: The change in energy for this Epoch.
    """
    energy_consumed = entity.parameters["metabolism_rate"]

    # Factor in resource availability
    resource_availability = environment_factors.get("resource_availability", 1.0)
    if resource_availability < 1.0:
        energy_consumed += (
            1.0 - resource_availability
        ) * 5  # More consumption if resources are low

    # Health also impacts energy consumption (e.g., sick entities use more energy)
    if entity.health < 50.0:
        energy_consumed += (50.0 - entity.health) * 0.1

    return -energy_consumed  # Energy decreases


def calculate_health_change(entity, environment_factors):
    """
    Calculates the change in an entity's health based on its energy level
    and environmental factors.

    Args:
        entity (Entity): The entity whose health is being calculated.
        environment_factors (dict): Current environmental conditions.

    Returns:
        float: The change in health for this Epoch.
    """
    health_change = 0.0

    # Energy impact on health
    if entity.energy > 50.0:
        health_change += (
            (entity.energy - 50.0) * entity.parameters["health_recovery_rate"] * 0.1
        )
    else:
        health_change -= (
            (50.0 - entity.energy) * entity.parameters["health_decay_rate"] * 0.1
        )

    # Environmental impact on health
    temperature = environment_factors.get("temperature", 25.0)
    pollution = environment_factors.get("pollution", 0.0)

    # Simple model: too hot/cold or pollution reduces health, mitigated by resilience
    if temperature < 10.0 or temperature > 35.0:
        health_change -= (
            abs(temperature - 22.5) * (1.0 - entity.parameters["resilience"]) * 0.1
        )

    if pollution > 0.1:
        health_change -= pollution * (1.0 - entity.parameters["resilience"]) * 5.0

    return health_change
