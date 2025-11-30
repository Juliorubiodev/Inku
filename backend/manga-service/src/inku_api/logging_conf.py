# src/inku_api/logging_conf.py
from typing import Any, Dict

def setup_logging(extra: Dict[str, Any] | None = None) -> None:
    """Configura logs. Si hay loguru, la usa; si no, cae a logging stdlib."""
    try:
        from loguru import logger as _logger  # type: ignore
        # Config básica de loguru
        _logger.remove()
        _logger.add(
            sink=lambda m: print(m, end=""),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}",
            level="INFO",
        )
        if extra:
            _logger = _logger.bind(**extra)  # rebind con extra por defecto
        globals()["logger"] = _logger
    except Exception:
        import logging, sys
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )
        globals()["logger"] = logging.getLogger("inku")

# logger “global” que el resto de módulos puede importar
try:
    from loguru import logger  # type: ignore
except Exception:
    import logging
    logger = logging.getLogger("inku")
