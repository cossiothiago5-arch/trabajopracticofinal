"""
Módulo principal - Punto de entrada de la aplicación.

Demuestra el funcionamiento del Sistema de Gestión de Biblioteca Digital
con todos los requisitos técnicos implementados.
"""

import sys
import os

# Agregar la ruta del proyecto al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patrones import Biblioteca
from personas import Usuario, Bibliotecario
from libros import Libro
from excepciones import PrestamoNoValido, LibroNoDisponible


def separador(titulo: str):
    """Imprime un separador visual en la consola."""
    print(f"\n{'='*70}")
    print(f"  {titulo}")
    print(f"{'='*70}\n")


def main():
    """Función principal que ejecuta demostraciones del sistema."""
    
    # ==================== DEMOSTRACIÓN 1: SINGLETON ====================
    separador("1. PATRÓN SINGLETON - Una única instancia de Biblioteca")
    
    biblioteca1 = Biblioteca("Biblioteca Municipal")
    biblioteca2 = Biblioteca("Otra Biblioteca")  # Intenta crear otra instancia
    
    print(f"biblioteca1 es biblioteca2: {biblioteca1 is biblioteca2}")
    print("✓ Ambas referencias apuntan a la misma instancia (SINGLETON)\n")
    
    biblioteca = biblioteca1  # Usamos la instancia única
    
    # ==================== DEMOSTRACIÓN 2: HERENCIA Y POLIMORFISMO ====================
    separador("2. HERENCIA Y POLIMORFISMO - Jerarquía de Personas")
    
    # Crear usuarios (heredan de Persona)
    usuario1 = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
    usuario2 = Usuario("María", "García", "87654321", "maria@email.com")
    
    # Crear bibliotecarios (heredan de Persona)
    bibliotecario = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com", "administrador")
    
    # Polimorfismo: el método __str__() se implementa diferente en cada clase
    print("Polimorfismo - método __str__() sobrescrito:\n")
    print(usuario1)
    print(usuario2)
    print(bibliotecario)
    
    print(f"\n✓ Cada clase implementa __str__() de manera diferente (POLIMORFISMO)")
    print(f"✓ Usuario y Bibliotecario heredan de Persona (HERENCIA)\n")
    
    # ==================== DEMOSTRACIÓN 3: AGREGACIÓN ====================
    separador("3. AGREGACIÓN - Biblioteca contiene Usuarios y Libros")
    
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)
    biblioteca.registrar_usuario(bibliotecario)
    
    # Crear libros
    libro1 = Libro("Clean Code", "Robert C. Martin", "978-0132350884", 2008, 464)
    libro2 = Libro("Design Patterns", "Gang of Four", "978-0201633610", 1994, 395)
    libro3 = Libro("Python Avanzado", "Raymond Hettinger", "978-1491927281", 2015, 320)
    
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)
    
    print("✓ Biblioteca contiene colecciones de Usuarios y Libros")
    print("✓ Estos elementos existen de forma independiente (AGREGACIÓN)\n")
    
    # ==================== DEMOSTRACIÓN 4: COMPOSICIÓN ====================
    separador("4. COMPOSICIÓN - Préstamo compuesto por Libro y Usuario")
    
    print("Creando préstamos (el Préstamo está compuesto por Libro + Usuario):\n")
    
    prestamo1 = biblioteca.registrar_prestamo(usuario1.dni, libro1.isbn)
    prestamo2 = biblioteca.registrar_prestamo(usuario2.dni, libro2.isbn)
    
    print("\n✓ Un Préstamo no tiene sentido sin sus componentes (Libro y Usuario)")
    print("✓ Relación fuerte entre componentes (COMPOSICIÓN)\n")
    
    # ==================== DEMOSTRACIÓN 5: DECORADORES ====================
    separador("5. DECORADORES PERSONALIZADOS")
    
    print("Los decoradores @registrar_operacion registran todas las operaciones:\n")
    print("Intentando devolver un libro (usa decorador @registrar_operacion):\n")
    
    multa = biblioteca.registrar_devolucion(prestamo1.id_prestamo)
    
    print("\n✓ Las operaciones están registradas automáticamente por el decorador\n")
    
    # ==================== DEMOSTRACIÓN 6: METACLASE ====================
    separador("6. METACLASE - Control de instancias del Singleton")
    
    print("Intentando crear múltiples instancias de Biblioteca:\n")
    
    bib_test1 = Biblioteca("Test 1")
    bib_test2 = Biblioteca("Test 2")
    bib_test3 = Biblioteca("Test 3")
    
    print(f"\nbib_test1 es bib_test2: {bib_test1 is bib_test2}")
    print(f"bib_test2 es bib_test3: {bib_test2 is bib_test3}")
    print("✓ El Singleton garantiza una única instancia\n")
    
    # ==================== DEMOSTRACIÓN 7: FUNCIONAMIENTO COMPLETO ====================
    separador("7. FUNCIONAMIENTO COMPLETO DEL SISTEMA")
    
    print("Estado actual de la biblioteca:\n")
    print(biblioteca)
    
    print("\n--- Libros disponibles ---")
    for libro in biblioteca.listar_libros_disponibles():
        print(f"  • {libro}")
    
    print("\n--- Usuarios registrados ---")
    for user in biblioteca.listar_usuarios():
        print(f"  • {user}")
    
    print("\n--- Estadísticas ---")
    stats = biblioteca.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")
    
    print("\n--- Préstamos activos de Juan Pérez ---")
    prestamos_juan = biblioteca.obtener_prestamos_activos(usuario1.dni)
    if prestamos_juan:
        for p in prestamos_juan:
            print(f"  • {p}")
    else:
        print("  (Sin préstamos activos)")
    
    # ==================== DEMOSTRACIÓN 8: MANEJO DE ERRORES ====================
    separador("8. MANEJO DE ERRORES Y VALIDACIONES")
    
    print("Intentando operaciones inválidas:\n")
    
    # Intentar prestar un libro no disponible
    try:
        print("1. Intentando prestar un libro prestado...")
        biblioteca.registrar_prestamo(usuario2.dni, libro2.isbn)  # Prestado a usuario2
    except Exception as e:
        print(f"   ✓ Excepción capturada: {e}\n")
    
    # Intentar prestar a un usuario con multa
    try:
        print("2. Intentando prestar a usuario con multa pendiente...")
        usuario1.aplicar_multa(50.0)
        biblioteca.registrar_prestamo(usuario1.dni, libro3.isbn)
    except Exception as e:
        print(f"   ✓ Excepción capturada: {e}\n")
    
    # ==================== CONCLUSIÓN ====================
    separador("REQUISITOS TÉCNICOS IMPLEMENTADOS")
    
    print("""
    ✅ HERENCIA
       • Clase base Persona
       • Clases derivadas: Usuario y Bibliotecario
       
    ✅ POLIMORFISMO
       • Método __str__() sobrescrito en múltiples clases
       • Diferentes comportamientos según el tipo
       
    ✅ AGREGACIÓN
       • Biblioteca contiene Usuarios y Libros
       • Relación débil: elementos existen independientemente
       
    ✅ COMPOSICIÓN
       • Préstamo compuesto por Libro y Usuario
       • Relación fuerte: no existe Préstamo sin sus componentes
       
    ✅ DECORADOR PERSONALIZADO
       • @registrar_operacion: registra operaciones del sistema
       • @validar_datos: valida tipos de datos
       
    ✅ METACLASE
       • MetaclaseSingleton: controla instancias
       • Implementada con type
       
    ✅ PATRÓN DE DISEÑO
       • Patrón SINGLETON para la clase Biblioteca
       • Garantiza una única instancia en la aplicación
    """)


if __name__ == "__main__":
    main()
    print("\n✓ Fin de la demostración\n")
