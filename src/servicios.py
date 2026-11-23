from abc import abstractmethod
from typing import Optional
from src.entidad import EntidadSistema
from src.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
    ServicioNoDisponibleError
)

class Servicio(EntidadSistema):
    """
    Clase abstracta base para los servicios ofrecidos por Software FJ.
    Implementa polimorfismo y simulación de sobrecarga mediante parámetros opcionales.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_base_hora = tarifa_base_hora
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def tarifa_base_hora(self) -> float:
        return self._tarifa_base_hora

    @tarifa_base_hora.setter
    def tarifa_base_hora(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise DatoInvalidoError(f"La tarifa base debe ser un número positivo. Recibido: {valor}")
        self._tarifa_base_hora = float(valor)

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado de disponibilidad debe ser booleano (True/False).")
        self._disponible = estado

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' ({self.id_entidad}) no está disponible actualmente.")

    def calcular_costo_total(
        self,
        horas: int,
        descuento_porcentaje: float = 0.0,
        impuesto_iva: float = 0.19,
        recargo_adicional: Optional[float] = None
    ) -> float:
        """
        Método sobrecargado funcionalmente mediante parámetros opcionales:
        Permite calcular costo simple, con descuento, con IVA personalizado o con recargos.
        """
        if not isinstance(horas, int) or horas <= 0:
            raise DatoInvalidoError("La duración en horas debe ser un entero mayor a cero.")
        if not (0 <= descuento_porcentaje <= 100):
            raise DatoInvalidoError("El porcentaje de descuento debe estar entre 0 y 100.")
        if impuesto_iva < 0:
            raise CalculoInconsistenteError("El impuesto IVA no puede ser negativo.")

        subtotal = self._calcular_subtotal_especifico(horas)
        if recargo_adicional is not None:
            if recargo_adicional < 0:
                raise CalculoInconsistenteError("El recargo adicional no puede ser negativo.")
            subtotal += recargo_adicional

        valor_descuento = subtotal * (descuento_porcentaje / 100.0)
        base_gravable = subtotal - valor_descuento
        total = base_gravable * (1 + impuesto_iva)

        if total < 0:
            raise CalculoInconsistenteError("El cálculo final arrojó un valor negativo inconsistente.")

        return round(total, 2)

    @abstractmethod
    def _calcular_subtotal_especifico(self, horas: int) -> float:
        """Método polimórfico que cada subclase implementa según su lógica de negocio."""
        pass

    @abstractmethod
    def validar_parametros_servicio(self, horas: int, **kwargs) -> bool:
        """Valida reglas específicas de cada tipo de servicio."""
        pass

    def validar_integridad(self) -> bool:
        return self._tarifa_base_hora > 0 and bool(self._nombre)


class ReservaSala(Servicio):
    """Servicio especializado 1: Alquiler de salas de conferencias o coworking."""
    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, capacidad_personas: int, tiene_videoconferencia: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base_hora)
        if not isinstance(capacidad_personas, int) or capacidad_personas < 2:
            raise DatoInvalidoError("La capacidad de una sala debe ser mínimo de 2 personas.")
        self.capacidad_personas = capacidad_personas
        self.tiene_videoconferencia = tiene_videoconferencia

    def _calcular_subtotal_especifico(self, horas: int) -> float:
        costo = self.tarifa_base_hora * horas
        # Recargo técnico por equipo de videoconferencia
        if self.tiene_videoconferencia:
            costo += 15000 * horas
        return costo

    def validar_parametros_servicio(self, horas: int, **kwargs) -> bool:
        asistentes = kwargs.get("asistentes", 1)
        if asistentes > self.capacidad_personas:
            raise DatoInvalidoError(
                f"Los asistentes ({asistentes}) superan la capacidad máxima de la sala ({self.capacidad_personas})."
            )
        return True

    def obtener_resumen(self) -> str:
        vc = "con Videoconferencia" if self.tiene_videoconferencia else "Estándar"
        return f"Sala [{self.id_entidad}] {self.nombre} | Cap: {self.capacidad_personas} pers. ({vc}) | Base: ${self.tarifa_base_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de hardware especializado (servidores, workstations)."""
    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, gama: str, deposito_garantia: float):
        super().__init__(id_servicio, nombre, tarifa_base_hora)
        if gama not in ("MEDIA", "ALTA", "ENTERPRISE"):
            raise DatoInvalidoError("La gama del equipo debe ser 'MEDIA', 'ALTA' o 'ENTERPRISE'.")
        if deposito_garantia < 0:
            raise DatoInvalidoError("El depósito de garantía no puede ser negativo.")
        self.gama = gama
        self.deposito_garantia = deposito_garantia

    def _calcular_subtotal_especifico(self, horas: int) -> float:
        factor_gama = {"MEDIA": 1.0, "ALTA": 1.25, "ENTERPRISE": 1.5}[self.gama]
        return (self.tarifa_base_hora * horas * factor_gama) + self.deposito_garantia

    def validar_parametros_servicio(self, horas: int, **kwargs) -> bool:
        if horas < 2:
            raise DatoInvalidoError("El alquiler de equipos requiere un mínimo de 2 horas.")
        return True

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}] {self.nombre} | Gama: {self.gama} | Garantía: ${self.deposito_garantia:,.0f}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría en ingeniería de software, nube o ciberseguridad."""
    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, especialidad: str, nivel_seniority: str):
        super().__init__(id_servicio, nombre, tarifa_base_hora)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe especificar el área de especialidad de la asesoría.")
        if nivel_seniority not in ("JUNIOR", "SEMI-SENIOR", "SENIOR", "ARQUITECTO"):
            raise DatoInvalidoError("Nivel de seniority inválido.")
        self.especialidad = especialidad.strip()
        self.nivel_seniority = nivel_seniority

    def _calcular_subtotal_especifico(self, horas: int) -> float:
        multiplicador = {"JUNIOR": 1.0, "SEMI-SENIOR": 1.3, "SENIOR": 1.6, "ARQUITECTO": 2.0}[self.nivel_seniority]
        return self.tarifa_base_hora * horas * multiplicador

    def validar_parametros_servicio(self, horas: int, **kwargs) -> bool:
        if horas > 40:
            raise DatoInvalidoError("Una asesoría individual no puede exceder 40 horas por reserva.")
        return True

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self.id_entidad}] {self.nombre} | Área: {self.especialidad} ({self.nivel_seniority})"
