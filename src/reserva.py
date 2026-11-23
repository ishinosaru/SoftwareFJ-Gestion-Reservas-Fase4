from datetime import datetime
from typing import List
from src.entidad import EntidadSistema
from src.cliente import Cliente
from src.servicios import Servicio
from src.excepciones import (
    ReservaInvalidaError,
    DatoInvalidoError,
    ErrorSistemaFJ
)

class Reserva(EntidadSistema):
    """
    Integra un Cliente, un Servicio, la duración y el ciclo de vida de estados
    (PENDIENTE -> CONFIRMADA -> PROCESADA / CANCELADA).
    """
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, fecha_inicio: datetime, duracion_horas: int, **parametros_extra):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")
        if not isinstance(fecha_inicio, datetime):
            raise DatoInvalidoError("La fecha de inicio debe ser un objeto datetime válido.")

        # Verificar disponibilidad y reglas propias del servicio (polimorfismo)
        servicio.verificar_disponibilidad()
        servicio.validar_parametros_servicio(duracion_horas, **parametros_extra)

        self.cliente = cliente
        self.servicio = servicio
        self.fecha_inicio = fecha_inicio
        self.duracion_horas = duracion_horas
        self._estado = "PENDIENTE"
        self._costo_final = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_final(self) -> float:
        return self._costo_final

    def confirmar(self):
        """Cambia el estado de PENDIENTE a CONFIRMADA y calcula el costo."""
        if self._estado != "PENDIENTE":
            raise ReservaInvalidaError(
                f"No se puede confirmar la reserva {self.id_entidad} porque está en estado '{self._estado}'."
            )
        # Aplicar 10% de descuento automático si el cliente es corporativo (uso de sobrecarga)
        descuento = 10.0 if self.cliente.es_corporativo else 0.0
        try:
            self._costo_final = self.servicio.calcular_costo_total(
                horas=self.duracion_horas,
                descuento_porcentaje=descuento
            )
            self._estado = "CONFIRMADA"
        except ErrorSistemaFJ as exc:
            # Encadenamiento de excepciones (raise ... from ...)
            raise ReservaInvalidaError(
                f"Fallo al confirmar la reserva {self.id_entidad} durante el cálculo financiero."
            ) from exc

    def procesar(self):
        """Ejecuta el servicio de una reserva previamente confirmada."""
        if self._estado != "CONFIRMADA":
            raise ReservaInvalidaError(
                f"Solo se pueden procesar reservas en estado CONFIRMADA. Estado actual: '{self._estado}'."
            )
        self.servicio.verificar_disponibilidad()
        self._estado = "PROCESADA"

    def cancelar(self, motivo: str = "Solicitud del cliente"):
        """Cancela una reserva siempre que no haya sido procesada."""
        if self._estado == "PROCESADA":
            raise ReservaInvalidaError(
                f"Imposible cancelar la reserva {self.id_entidad}: el servicio ya fue PROCESADO."
            )
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id_entidad} ya se encontraba cancelada.")
        self._estado = "CANCELADA"

    def validar_integridad(self) -> bool:
        return self._estado in self.ESTADOS_VALIDOS and self.duracion_horas > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Horas: {self.duracion_horas} | "
            f"Estado: {self._estado} | Total: ${self._costo_final:,.2f}"
        )


class GestorSoftwareFJ:
    """
    Contenedor en memoria (listas internas sin base de datos) que administra
    clientes, servicios y reservas de Software FJ.
    """
    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente):
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):
            raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.")
        self.clientes.append(cliente)

    def registrar_servicio(self, servicio: Servicio):
        if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
            raise DatoInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.")
        self.servicios.append(servicio)

    def crear_reserva(self, reserva: Reserva):
        # Validar cruce de horarios para el mismo servicio en reservas activas
        for r in self.reservas:
            if r.servicio.id_entidad == reserva.servicio.id_entidad and r.estado in ("PENDIENTE", "CONFIRMADA"):
                if r.fecha_inicio == reserva.fecha_inicio:
                    raise ReservaInvalidaError(
                        f"Conflicto de horario: el servicio '{reserva.servicio.nombre}' ya está reservado en esa fecha/hora."
                    )
        self.reservas.append(reserva)
