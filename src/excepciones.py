class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados de Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        self.codigo_error = codigo_error
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro tiene formato, tipo o valor incorrecto."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR-DATO-001")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un dato obligatorio para crear una entidad o reserva."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR-PARAM-002")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin capacidad."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR-SERV-003")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante conflictos de horario, duración inválida o cambios de estado prohibidos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR-RES-004")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de tarifas arroja valores negativos o incoherentes."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR-CALC-005")
