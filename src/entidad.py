from abc import ABC, abstractmethod
from datetime import datetime
from src.excepciones import ParametroFaltanteError, DatoInvalidoError

class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad gestionable
    dentro del sistema de Software FJ. Aplica abstracción y encapsulación.
    """
    def __init__(self, id_entidad: str):
        self.id_entidad = id_entidad
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El identificador de la entidad no puede estar vacío.")
        if len(valor.strip()) < 3:
            raise DatoInvalidoError(f"El ID '{valor}' debe tener al menos 3 caracteres.")
        self._id_entidad = valor.strip().upper()

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Método abstracto obligatorio para verificar que el objeto sea consistente."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para representar textualmente la entidad."""
        pass
