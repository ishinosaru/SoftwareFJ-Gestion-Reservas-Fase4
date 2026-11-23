# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

Proyecto desarrollado de manera individual para el componente práctico (Fase 4) del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Características Principales
- **Arquitectura Orientada a Objetos:** Abstracción (`ABC`), herencia, polimorfismo, encapsulación mediante `@property` y métodos sobrecargados mediante parámetros opcionales.
- **Sin Bases de Datos:** Gestión integral en memoria utilizando listas y objetos en tiempo de ejecución.
- **Manejo Avanzado de Excepciones:** Jerarquía de excepciones propias (`ErrorSistemaFJ`), bloques `try/except/else/finally` y encadenamiento (`raise ... from ...`).
- **Auditoría y Trazabilidad:** Registro automático de eventos y errores en `logs/sistema_software_fj.log`.

## Ejecución
```bash
python main.py
