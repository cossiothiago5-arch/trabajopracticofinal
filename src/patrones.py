"""
Módulo de patrones de diseño para el sistema de gestión de biblioteca digital.

Implementa el patrón Singleton para la clase Biblioteca.
"""

from typing import List, Dict, Optional
from datetime import datetime


class Biblioteca:
    """
    Clase que representa la Biblioteca Digital del sistema (Singleton).
    
    Utiliza AGREGACIÓN:
    - Contiene colecciones de Libros y Usuarios
    """
    
    _instancia = None
    
    def __new__(cls, nombre: str = "Biblioteca Digital"):
        """Implementa Singleton sin metaclase."""
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia
    
    def __init__(self, nombre: str = "Biblioteca Digital"):
        """Inicializa la instancia única de la Biblioteca."""
        if self._inicializado:
            return
            
        self.nombre = nombre
        self.libros: Dict[str, 'Libro'] = {}
        self.usuarios: Dict[str, 'Usuario'] = {}
        self.prestamos: Dict[str, 'Prestamo'] = {}
        self.prestamos_historial: List['Prestamo'] = []
        self._inicializado = True
        print(f"✓ Biblioteca '{self.nombre}' inicializada (Singleton Pattern)")
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def agregar_libro(self, libro: 'Libro') -> bool:
        """Agrega un nuevo libro a la biblioteca."""
        if libro.isbn in self.libros:
            raise ValueError(f"El libro con ISBN {libro.isbn} ya existe")
        
        self.libros[libro.isbn] = libro
        print(f"✓ Libro '{libro.titulo}' agregado a la biblioteca")
        return True
    
    def eliminar_libro(self, isbn: str) -> bool:
        """Elimina un libro de la biblioteca."""
        if isbn not in self.libros:
            raise ValueError(f"Libro con ISBN {isbn} no encontrado")
        
        libro = self.libros[isbn]
        if not libro.disponible:
            raise ValueError(f"No se puede eliminar '{libro.titulo}': tiene un préstamo activo")
        
        del self.libros[isbn]
        print(f"✓ Libro '{libro.titulo}' eliminado de la biblioteca")
        return True
    
    def buscar_libro_por_isbn(self, isbn: str) -> Optional['Libro']:
        """Busca un libro por ISBN."""
        return self.libros.get(isbn)
    
    def buscar_libro_por_titulo(self, titulo: str) -> List['Libro']:
        """Busca libros por título (búsqueda parcial)."""
        titulo_lower = titulo.lower()
        return [libro for libro in self.libros.values() 
                if titulo_lower in libro.titulo.lower()]
    
    def listar_libros_disponibles(self) -> List['Libro']:
        """Lista todos los libros disponibles para préstamo."""
        return [libro for libro in self.libros.values() if libro.disponible]
    
    def listar_todos_libros(self) -> List['Libro']:
        """Lista todos los libros en la biblioteca."""
        return sorted(self.libros.values(), key=lambda x: x.titulo)
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def registrar_usuario(self, usuario: 'Usuario') -> bool:
        """Registra un nuevo usuario en la biblioteca."""
        if usuario.dni in self.usuarios:
            raise ValueError(f"Usuario con DNI {usuario.dni} ya existe")
        
        self.usuarios[usuario.dni] = usuario
        print(f"✓ Usuario '{usuario.obtener_nombre_completo()}' registrado")
        return True
    
    def eliminar_usuario(self, dni: str) -> bool:
        """Elimina un usuario de la biblioteca."""
        if dni not in self.usuarios:
            raise ValueError(f"Usuario con DNI {dni} no encontrado")
        
        usuario = self.usuarios[dni]
        if usuario.prestamos_activos > 0:
            raise ValueError(f"{usuario.obtener_nombre_completo()} tiene préstamos activos")
        
        del self.usuarios[dni]
        print(f"✓ Usuario '{usuario.obtener_nombre_completo()}' eliminado")
        return True
    
    def buscar_usuario_por_dni(self, dni: str) -> Optional['Usuario']:
        """Busca un usuario por DNI."""
        return self.usuarios.get(dni)
    
    def listar_usuarios(self) -> List['Usuario']:
        """Lista todos los usuarios registrados."""
        return list(self.usuarios.values())
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def registrar_prestamo(self, dni_usuario: str, isbn_libro: str) -> 'Prestamo':
        """Registra un nuevo préstamo de un libro a un usuario."""
        usuario = self.buscar_usuario_por_dni(dni_usuario)
        if not usuario:
            raise ValueError(f"Usuario con DNI {dni_usuario} no encontrado")
        
        libro = self.buscar_libro_por_isbn(isbn_libro)
        if not libro:
            raise ValueError(f"Libro con ISBN {isbn_libro} no encontrado")
        
        if not libro.disponible:
            raise ValueError(f"El libro '{libro.titulo}' no está disponible")
        
        # Importar aquí para evitar circular import
        from src.prestamos import Prestamo
        
        prestamo = Prestamo(libro, usuario)
        self.prestamos[prestamo.id_prestamo] = prestamo
        self.prestamos_historial.append(prestamo)
        
        print(f"✓ Préstamo {prestamo.id_prestamo} registrado: "
              f"'{libro.titulo}' → {usuario.obtener_nombre_completo()}")
        return prestamo
    
    def registrar_devolucion(self, id_prestamo: str) -> float:
        """Registra la devolución de un libro prestado."""
        if id_prestamo not in self.prestamos:
            raise ValueError(f"Préstamo {id_prestamo} no encontrado")
        
        prestamo = self.prestamos[id_prestamo]
        multa = prestamo.registrar_devolucion()
        
        del self.prestamos[id_prestamo]
        
        print(f"✓ Devolución registrada: {prestamo.libro.titulo} "
              f"← {prestamo.usuario.obtener_nombre_completo()}")
        if multa > 0:
            print(f"  ⚠ Multa por retraso: ${multa:.2f}")
        
        return multa
    
    def obtener_prestamos_activos(self, dni_usuario: str) -> List['Prestamo']:
        """Obtiene todos los préstamos activos de un usuario."""
        usuario = self.buscar_usuario_por_dni(dni_usuario)
        if not usuario:
            raise ValueError(f"Usuario con DNI {dni_usuario} no encontrado")
        
        return [p for p in self.prestamos.values() if p.usuario.dni == dni_usuario]
    
    def listar_prestamos_retrasados(self) -> List['Prestamo']:
        """Lista todos los préstamos retrasados."""
        return [p for p in self.prestamos.values() if p.esta_retrasado()]
    
    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas generales de la biblioteca."""
        return {
            "total_libros": len(self.libros),
            "libros_disponibles": len(self.listar_libros_disponibles()),
            "libros_prestados": len(self.libros) - len(self.listar_libros_disponibles()),
            "total_usuarios": len(self.usuarios),
            "prestamos_activos": len(self.prestamos),
            "prestamos_historial": len(self.prestamos_historial),
            "prestamos_retrasados": len(self.listar_prestamos_retrasados())
        }
    
    def __str__(self) -> str:
        """Representación en string de la biblioteca."""
        stats = self.obtener_estadisticas()
        return (f"📖 {self.nombre}\n"
                f"  Libros: {stats['libros_disponibles']}/{stats['total_libros']} disponibles\n"
                f"  Usuarios: {stats['total_usuarios']}\n"
                f"  Préstamos activos: {stats['prestamos_activos']}")
    
    @classmethod
    def obtener_instancia(cls, nombre: str = "Biblioteca Digital") -> 'Biblioteca':
        """Obtiene la instancia única de Biblioteca."""
        if cls._instancia is None:
            cls._instancia = cls(nombre)
        return cls._instancia
