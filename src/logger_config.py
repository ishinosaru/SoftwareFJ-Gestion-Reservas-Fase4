import logging
import os

def configurar_logger():
    """
    Configura el sistema de logging para registrar tanto eventos informativos
    como errores críticos en un archivo de texto plano sin detener la ejecución.
    """
    # Crear carpeta de logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar manejadores si se llama varias veces
    if not logger.handlers:
        # Manejador de archivo para guardar historial persistente
        file_handler = logging.FileHandler("logs/sistema_software_fj.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Formato detallado con fecha, nivel y mensaje
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
