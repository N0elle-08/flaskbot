from build.actions import Actions
from settings.base import setup_logger

actions = Actions()
logger = setup_logger()

def funct_call(name, args):
    if name == "create_incident":
        logger.info(f"create_incident {args}")
        return actions.create_incident(args)



