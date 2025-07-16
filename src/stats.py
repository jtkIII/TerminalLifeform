from colored import Back, Fore, Style

from entity import Entity
from logging_config import setup_logger

logger = setup_logger(__name__)

final_totals = {
    "total_entities": 0,
    "total_deaths": 0,
    "total_births": 0,
    "total_alive_at_conclusion": 0,
    "total_struggling": 0,
    "total_thriving": 0,
    "total_events": 0,
    "total_disasters": 0,
    "total_mutations": 0,
    "total_interactions": 0,
}


def update_totals(total: int, alive: int, struggling: int, thriving: int):
    """
    Update the final totals based on the current state of entities.
    """
    final_totals["total_entities"] = total
    final_totals["total_alive_at_conclusion"] = alive
    final_totals["total_struggling"] = struggling
    final_totals["total_thriving"] = thriving

    finalize_totals()


def finalize_totals():
    """
    Finalize and log the total counts of entities at the end of the simulation.
    """
    logger.info(
        "\n"
        f"{Fore.green}Total Entities:{Style.reset} {final_totals['total_entities']}, "
        f"{Fore.green}Total Deaths:{Style.reset} {final_totals['total_deaths']}, "
        f"{Fore.green}Total Births:{Style.reset} {final_totals['total_births']}, "
        f"{Fore.green}Total Mutations:{Style.reset} {final_totals['total_mutations']}, "
        "\n --- Summary ---"
        f"{Fore.green}Alive at Conclusion:{Style.reset} {final_totals['total_alive_at_conclusion']}, "
        f"{Fore.green}Thriving:{Style.reset} {final_totals['total_thriving']}, "
        f"{Fore.green}Struggling:{Style.reset} {final_totals['total_struggling']}"
        # f"{Fore.green}, Total Disasters:{Style.reset} {final_totals['total_disasters']}, "
        # f"{Fore.green}Total Interactions:{Style.reset} {final_totals['total_interactions']}"
    )


def death_tracker(entity: Entity):
    """
    Track the death of an entity and log its details.
    """
    logger.info(
        f"{Back.yellow}{entity.id} - {entity.name} died. (Age:{entity.age}) {Style.reset}"
    )

    final_totals["total_deaths"] += 1


def birth_tracker(entity, new_entity, time):
    """
    Track the birth of an entity and log its details.
    """
    logger.info(
        f"{Back.red}Time {time}: Entity {entity.id} reproduced! New entity {new_entity.id} - {new_entity.name} born.{Style.reset}"
    )

    final_totals["total_births"] += 1


def disaster_tracker(event_type: str, time: int, name: str = None):
    """
    Track a disaster event and log its details.
    """
    logger.warning(
        f"{Fore.blue}Disaster Event: {event_type} occurred at time {time} - {name} died {Style.reset} "
    )
    final_totals["total_disasters"] += 1


def mutation_tracker(name: str, original_value: float, new_value: float):
    """
    Track a mutation event and log its details.
    """
    logger.info(
        f"{Fore.green}Mutation Event: {name} mutated! Original Value: {original_value} - New Value: {new_value}.{Style.reset}"
    )
    final_totals["total_mutations"] += 1
