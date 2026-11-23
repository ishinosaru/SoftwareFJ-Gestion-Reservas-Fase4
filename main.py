from datetime import datetime
from src.logger_config import configurar_logger
from src.cliente import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.reserva import Reserva, GestorSoftwareFJ
from src.excepciones import ErrorSistemaFJ

def ejecutar_simulacion():
    logger = configurar_logger()
    sistema = GestorSoftwareFJ()

    print("=" * 75)
    print(" SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 75)
    logger.info("INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de cliente corporativo (try / except / else)
    # -------------------------------------------------------------------------
    try:
        c1 = Cliente("CLI-001", "Laura Gómez", "laura.gomez@techcorp.co", "3104567890", es_corporativo=True)
        sistema.registrar_cliente(c1)
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 1 fallida: {e}")
    else:
        msg = f"[OK] Operación 1: {c1.obtener_resumen()}"
        print(msg)
        logger.info(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de cliente particular
    # -------------------------------------------------------------------------
    try:
        c2 = Cliente("CLI-002", "Carlos Mendoza", "cmendoza@correo.com", "3209876543", es_corporativo=False)
        sistema.registrar_cliente(c2)
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 2 fallida: {e}")
    else:
        msg = f"[OK] Operación 2: {c2.obtener_resumen()}"
        print(msg)
        logger.info(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro INVÁLIDO de cliente (correo y nombre mal formados)
    # -------------------------------------------------------------------------
    try:
        c_err = Cliente("CLI-003", "Juan123", "correo-sin-arroba.com", "123")
        sistema.registrar_cliente(c_err)
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 3 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Creación válida de 3 servicios especializados (Polimorfismo)
    # -------------------------------------------------------------------------
    try:
        s_sala = ReservaSala("SRV-101", "Sala Innovación Norte", 80000, capacidad_personas=10, tiene_videoconferencia=True)
        s_equipo = AlquilerEquipo("SRV-201", "Workstation IA RTX-4090", 45000, gama="ENTERPRISE", deposito_garantia=100000)
        s_asesoria = AsesoriaEspecializada("SRV-301", "Arquitectura Cloud AWS", 120000, especialidad="Cloud Computing", nivel_seniority="ARQUITECTO")

        sistema.registrar_servicio(s_sala)
        sistema.registrar_servicio(s_equipo)
        sistema.registrar_servicio(s_asesoria)
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 4 fallida: {e}")
    else:
        print("[OK] Operación 4: Tres servicios especializados creados y registrados:")
        for srv in sistema.servicios:
            print("   ->", srv.obtener_resumen())
            logger.info(f"Servicio registrado: {srv.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación INVÁLIDA de servicio (tarifa negativa)
    # -------------------------------------------------------------------------
    try:
        s_err = ReservaSala("SRV-999", "Sala Fantasma", -50000, capacidad_personas=5)
        sistema.registrar_servicio(s_err)
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 5 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Reserva EXITOSA de Sala + Confirmación + Procesamiento
    # -------------------------------------------------------------------------
    fecha_1 = datetime(2026, 11, 25, 9, 0)
    try:
        r1 = Reserva("RES-001", c1, s_sala, fecha_1, duracion_horas=4, asistentes=8)
        sistema.crear_reserva(r1)
        r1.confirmar()
        r1.procesar()
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 6 fallida: {e}")
    else:
        msg = f"[OK] Operación 6: {r1.obtener_resumen()}"
        print(msg)
        logger.info(msg)
    finally:
        logger.debug("Bloque finally ejecutado tras Operación 6 (auditoría de transacción).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Reserva FALLIDA por exceso de capacidad en sala
    # -------------------------------------------------------------------------
    try:
        r2 = Reserva("RES-002", c2, s_sala, datetime(2026, 11, 26, 14, 0), duracion_horas=2, asistentes=25)
        sistema.crear_reserva(r2)
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 7 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Reserva EXITOSA de Alquiler de Equipo + Cancelación controlada
    # -------------------------------------------------------------------------
    try:
        r3 = Reserva("RES-003", c2, s_equipo, datetime(2026, 11, 27, 10, 0), duracion_horas=5)
        sistema.crear_reserva(r3)
        r3.confirmar()
        r3.cancelar("Cambio de cronograma del cliente")
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 8 fallida: {e}")
    else:
        msg = f"[OK] Operación 8: {r3.obtener_resumen()}"
        print(msg)
        logger.info(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Intento INVÁLIDO de cancelar una reserva ya PROCESADA
    # -------------------------------------------------------------------------
    try:
        r1.cancelar("Intento tardío de cancelación")
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 9 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva EXITOSA de Asesoría + Prueba de Sobrecarga de Costos
    # -------------------------------------------------------------------------
    try:
        r4 = Reserva("RES-004", c1, s_asesoria, datetime(2026, 11, 28, 8, 0), duracion_horas=3)
        sistema.crear_reserva(r4)
        r4.confirmar()
        # Uso directo de sobrecarga con recargo adicional por urgencia
        costo_urgente = s_asesoria.calcular_costo_total(horas=3, descuento_porcentaje=5.0, recargo_adicional=50000)
    except ErrorSistemaFJ as e:
        logger.error(f"Operación 10 fallida: {e}")
    else:
        msg = f"[OK] Operación 10: {r4.obtener_resumen()} | Cotización urgente: ${costo_urgente:,.2f}"
        print(msg)
        logger.info(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva FALLIDA por servicio no disponible
    # -------------------------------------------------------------------------
    try:
        s_equipo.disponible = False  # Se inhabilita temporalmente por mantenimiento
        r5 = Reserva("RES-005", c1, s_equipo, datetime(2026, 11, 29, 9, 0), duracion_horas=4)
        sistema.crear_reserva(r5)
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 11 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Reserva FALLIDA por conflicto de horario en Asesoría
    # -------------------------------------------------------------------------
    try:
        r6 = Reserva("RES-006", c2, s_asesoria, datetime(2026, 11, 28, 8, 0), duracion_horas=2)
        sistema.crear_reserva(r6)
    except ErrorSistemaFJ as e:
        msg = f"[CONTROLADO] Operación 12 rechazada correctamente -> {e}"
        print(msg)
        logger.warning(msg)

    print("=" * 75)
    print(f"RESUMEN EN MEMORIA -> Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)}")
    print("Log detallado guardado en: logs/sistema_software_fj.log")
    print("=" * 75)
    logger.info("FIN DE SIMULACIÓN SIN INTERRUPCIONES.")

if __name__ == "__main__":
    ejecutar_simulacion()
