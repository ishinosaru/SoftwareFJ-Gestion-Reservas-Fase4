import re
from src.entidad import EntidadSistema
from src.excepciones import DatoInvalidoError, ParametroFaltanteError

class Cliente(EntidadSistema):
    """
    Representa un cliente de Software FJ con validación estricta
    y encapsulación de sus datos personales.
    """
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str, es_corporativo: bool = False):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._es_corporativo = bool(es_corporativo)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3 or any(char.isdigit() for char in valor):
            raise DatoInvalidoError(f"Nombre inválido '{valor}': no debe contener números y requiere mínimo 3 letras.")
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor.strip()):
            raise DatoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El teléfono es obligatorio.")
        digitos = re.sub(r"\D", "", valor)
        if len(digitos) < 7 or len(digitos) > 15:
            raise DatoInvalidoError(f"Número de teléfono inválido '{valor}': debe tener entre 7 y 15 dígitos.")
        self._telefono = digitos

    @property
    def es_corporativo(self) -> bool:
        return self._es_corporativo

    def validar_integridad(self) -> bool:
        return all([self._id_entidad, self._nombre, self._correo, self._telefono])

    def obtener_resumen(self) -> str:
        tipo = "Corporativo" if self._es_corporativo else "Particular"
        return f"Cliente [{self.id_entidad}] {self.nombre} ({tipo}) - Email: {self.correo}"
