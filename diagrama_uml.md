""""
Diagrama UML del Sistema de Gestión de Biblioteca Digital

DESCRIPCIÓN DE RELACIONES:
- Herencia (--▶): Relación "es-un"
- Agregación (◇---): Relación "tiene-muchos" (débil)
- Composición (◆---): Relación "está-compuesto-por" (fuerte)
"""

# DIAGRAMA UML EN TEXTO

diagram = """
╔════════════════════════════════════════════════════════════════════════════╗
║              DIAGRAMA UML - SISTEMA DE GESTIÓN DE BIBLIOTECA              ║
╚════════════════════════════════════════════════════════════════════════════╝

                                    ┌─────────────┐
                                    │   Persona   │ (Clase Abstracta)
                                    ├─────────────┤
                                    │ - nombre    │
                                    │ - apellido  │
                                    │ - dni       │
                                    │ - email     │
                                    ├─────────────┤
                                    │ + obtener_tipo()
                                    │ + obtener_permisos()
                                    │ + __str__()
                                    └──────┬──────┘
                                           │ HERENCIA
                        ┌──────────────────┴──────────────────┐
                        │                                     │
                    ┌─────────┐                         ┌──────────────┐
                    │ Usuario │                         │ Bibliotecario│
                    ├─────────┤                         ├──────────────┤
                    │- estado │                         │-numero_empl. │
                    │- multa  │                         │-nivel_acceso │
                    └─────────┘                         └──────────────┘


                              ┌──────────────┐
                              │    Libro     │
                              ├──────────────┤
                              │- titulo      │
                              │- autor       │
                              │- isbn        │
                              │- anio_publ.  │
                              │- paginas     │
                              │- disponible  │
                              └──────────────┘


                    ┌──────────────────────┐
                    │    Préstamo          │ (COMPOSICIÓN)
                    ├──────────────────────┤
                    │◆ libro: Libro        │ ◄───── RELACIÓN FUERTE
                    │◆ usuario: Usuario    │ ◄───── (Sin libro/usuario
                    │- fecha_prestamo      │        no hay préstamo)
                    │- fecha_devolucion    │
                    │- estado              │
                    └──────────────────────┘


                              ┌──────────────────┐
                              │   Biblioteca     │ (Singleton)
                              ├──────────────────┤
                              │- nombre          │
                              │◇ libros: dict    │ ◄───── AGREGACIÓN
                              │◇ usuarios: dict  │ ◄───── (Relación débil)
                              │◇ prestamos: dict │
                              ├──────────────────┤
                              │+ agregar_libro() │
                              │+ registrar_usuario()
                              │+ registrar_prestamo()
                              │+ registrar_devolucion()
                              └──────────────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                          LEYENDA DE RELACIONES                             ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  HERENCIA (--▶):     Usuario --▶ Persona                                  ║
║                      "Usuario ES-UN Persona"                               ║
║                                                                            ║
║  AGREGACIÓN (◇---):  Biblioteca ◇--- Libro                                ║
║                      "Biblioteca TIENE libros"                             ║
║                      (los libros pueden existir sin biblioteca)             ║
║                                                                            ║
║  COMPOSICIÓN (◆---): Préstamo ◆--- Libro                                  ║
║                      "Préstamo ESTÁ-COMPUESTO-POR libro"                   ║
║                      (el libro no existe sin préstamo)                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


╔════════════════════════════════════════════════════════════════════════════╗
║                    REQUISITOS TÉCNICOS IMPLEMENTADOS                       ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  1. HERENCIA:                                                              ║
║     • Persona (clase base abstracta)                                       ║
║     • Usuario (heredado de Persona)                                        ║
║     • Bibliotecario (heredado de Persona)                                  ║
║                                                                            ║
║  2. POLIMORFISMO:                                                          ║
║     • Método __str__() sobrescrito en Usuario y Bibliotecario              ║
║     • Cada clase tiene su propia implementación                            ║
║                                                                            ║
║  3. AGREGACIÓN:                                                            ║
║     • Biblioteca contiene colecciones de Libros y Usuarios                 ║
║     • Relación débil: elementos pueden existir independientemente          ║
║                                                                            ║
║  4. COMPOSICIÓN:                                                           ║
║     • Préstamo compuesto por Libro y Usuario                               ║
║     • Relación fuerte: no existe Préstamo sin sus componentes              ║
║                                                                            ║
║  5. DECORADOR:                                                             ║
║     • @registrar_operacion: registra operaciones del sistema               ║
║     • @validar_datos: valida tipos antes de asignar                        ║
║                                                                            ║
║  6. METACLASE:                                                             ║
║     • MetaclaseSingleton: implementada con type                            ║
║     • Controla la creación de instancias de Biblioteca                     ║
║                                                                            ║
║  7. PATRÓN DE DISEÑO:                                                      ║
║     • Patrón SINGLETON: una única instancia de Biblioteca                  ║
║     • Implementado mediante MetaclaseSingleton                             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


╔════════════════════════════════════════════════════════════════════════════╗
║                         MÉTODOS PRINCIPALES                               ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  CLASE BIBLIOTECA (Singleton):                                             ║
║  ├─ agregar_libro(libro)                                                  ║
║  ├─ eliminar_libro(isbn)                                                  ║
║  ├─ modificar_libro(isbn, **kwargs)                                       ║
║  ├─ registrar_usuario(usuario)                                            ║
║  ├─ eliminar_usuario(dni)                                                 ║
║  ├─ registrar_prestamo(dni_usuario, isbn_libro)                           ║
║  ├─ registrar_devolucion(id_prestamo)                                     ║
║  ├─ listar_libros_disponibles()                                           ║
║  ├─ obtener_prestamos_activos(dni_usuario)                                ║
║  └─ obtener_estadisticas()                                                ║
║                                                                            ║
║  CLASE PRÉSTAMO (Composición):                                             ║
║  ├─ calcular_dias_retraso()                                               ║
║  ├─ calcular_multa()                                                      ║
║  ├─ registrar_devolucion()                                                ║
║  └─ esta_retrasado()                                                      ║
║                                                                            ║
║  CLASE USUARIO (Herencia):                                                ║
║  ├─ puede_realizar_prestamo()                                             ║
║  ├─ incrementar_prestamos()                                               ║
║  ├─ aplicar_multa(cantidad)                                               ║
║  └─ obtener_permisos()                                                    ║
║                                                                            ║
║  CLASE BIBLIOTECARIO (Herencia):                                          ║
║  ├─ tiene_permiso(permiso)                                                ║
║  ├─ registrar_operacion()                                                 ║
║  └─ obtener_permisos()                                                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

print(diagram)
