from colored import Back, Fore, Style

from entity import Entity
from logging_config import setup_logger

logger = setup_logger(__name__)


def death_tracker(entity: Entity):
    """
    Track the death of an entity and log its details.
    TODO: Build dictionary of dead entities with their details.
    This can be used for further analysis or reporting.
    """
    logger.info(
        f"{Back.yellow}{entity.id} - {entity.name} died. (Age:{entity.age}) {Style.reset}"
    )


def birth_tracker(entity, new_entity, time):
    """
    Track the birth of an entity and log its details.
    TODO: Build dictionary of born entities with their details.
    This can be used for further analysis or reporting.
    """
    logger.info(
        f"{Back.red}Time {time}: Entity {entity.id} reproduced! New entity {new_entity.id} - {new_entity.name} born.{Style.reset}"
    )
