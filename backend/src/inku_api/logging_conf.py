from loguru import logger
import sys

def setup_logging(debug: bool = False) -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG" if debug else "INFO",
        backtrace=debug,
        diagnose=debug,
        serialize=False,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "{message} | {extra}",
    )
