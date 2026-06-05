"""
Pruebas unitarias para el Sistema de Gestión de Biblioteca Digital.

Verifica que todas las clases funcionan correctamente y cumplen
con los requisitos funcionales especificados.
"""

import pytest
from src.patrones import Biblioteca
from src.personas import Usuario, Bibliotecario, Persona
from src.libros import Libro
from src.prestamos import Prestamo
from src.excepciones import (
    LibroNoEncontrado, UsuarioNoEncontrado, PrestamoNoValido,
    LibroNoDisponible, DevolucioNoEncontrada
)
from src.metaclases import MetaclaseSingleton


class TestBibliotecaSingleton:
    """Pruebas para verificar que Biblioteca usa Singleton correctamente."""
    
    def setup_method(self):
        """Resetea las instancias antes de cada prueba."""
        MetaclaseSingleton._instancias.clear()
    
    def test_singleton_misma_instancia(self):
        """Verifica que se devuelve la misma instancia del Singleton."""
        bib1 = Biblioteca("Test")
        bib2 = Biblioteca("Otra")
        assert bib1 is bib2
    
    def test_singleton_nombre_primera_instancia(self):
        """Verifica que el nombre es el de la primera instancia."""
        bib1 = Biblioteca("Primera")
        bib2 = Biblioteca("Segunda")
        assert bib1.nombre == "Primera"
        assert bib2.nombre == "Primera"


class TestLibro:
    """Pruebas para la clase Libro."""
    
    def test_crear_libro_valido(self):
        """Verifica que se puede crear un libro con datos válidos."""
        libro = Libro("Clean Code", "Robert Martin", "978-0132350884", 2008, 464)
        assert libro.titulo == "Clean Code"
        assert libro.autor == "Robert Martin"
        assert libro.disponible is True
    
    def test_libro_titulo_vacio_error(self):
        """Verifica que error al crear libro sin título."""
        with pytest.raises(ValueError):
            Libro("", "Autor", "ISBN", 2008, 100)
    
    def test_libro_ano_invalido_error(self):
        """Verifica que error con año de publicación inválido."""
        with pytest.raises(ValueError):
            Libro("Título", "Autor", "ISBN", 500, 100)
    
    def test_libro_marcar_como_prestado(self):
        """Verifica que se puede marcar un libro como prestado."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        libro.marcar_como_prestado("PREST000001")
        assert libro.disponible is False
        assert libro.prestamo_activo == "PREST000001"
    
    def test_libro_marcar_como_disponible(self):
        """Verifica que se puede marcar un libro como disponible."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        libro.marcar_como_prestado("PREST000001")
        libro.marcar_como_disponible()
        assert libro.disponible is True


class TestUsuario:
    """Pruebas para la clase Usuario."""
    
    def test_crear_usuario(self):
        """Verifica que se puede crear un usuario."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        assert usuario.nombre == "Juan"
        assert usuario.estado == "activo"
        assert usuario.prestamos_activos == 0
    
    def test_usuario_puede_realizar_prestamo(self):
        """Verifica que usuario activo sin multa puede prestar."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        assert usuario.puede_realizar_prestamo() is True
    
    def test_usuario_con_multa_no_puede_prestar(self):
        """Verifica que usuario con multa no puede prestar."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        usuario.aplicar_multa(50.0)
        assert usuario.puede_realizar_prestamo() is False
    
    def test_usuario_incrementar_decrementar_prestamos(self):
        """Verifica conteo de préstamos activos."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        usuario.incrementar_prestamos()
        assert usuario.prestamos_activos == 1
        usuario.decrementar_prestamos()
        assert usuario.prestamos_activos == 0


class TestBibliotecario:
    """Pruebas para la clase Bibliotecario."""
    
    def test_crear_bibliotecario(self):
        """Verifica que se puede crear un bibliotecario."""
        bib = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com")
        assert bib.obtener_tipo() == "Bibliotecario"
        assert "BIB" in bib.numero_empleado
    
    def test_bibliotecario_permisos_basicos(self):
        """Verifica permisos de bibliotecario básico."""
        bib = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com", "basico")
        permisos = bib.obtener_permisos()
        assert "agregar_libro" in permisos
        assert "administrar_bibliotecarios" not in permisos
    
    def test_bibliotecario_permisos_administrador(self):
        """Verifica permisos de administrador."""
        bib = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com", "administrador")
        permisos = bib.obtener_permisos()
        assert "administrar_bibliotecarios" in permisos
        assert "configurar_sistema" in permisos


class TestPrestamo:
    """Pruebas para la clase Préstamo."""
    
    def test_crear_prestamo_valido(self):
        """Verifica que se puede crear un préstamo válido."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        prestamo = Prestamo(libro, usuario)
        assert prestamo.estado == "activo"
        assert libro.disponible is False
    
    def test_prestamo_libro_no_disponible_error(self):
        """Verifica error al intentar prestar libro no disponible."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        usuario1 = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        usuario2 = Usuario("María", "García", "87654321", "maria@email.com")
        
        prestamo1 = Prestamo(libro, usuario1)
        with pytest.raises(PrestamoNoValido):
            prestamo2 = Prestamo(libro, usuario2)
    
    def test_prestamo_usuario_sin_permiso_error(self):
        """Verifica error con usuario que no puede prestar."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        usuario.aplicar_multa(50.0)
        
        with pytest.raises(PrestamoNoValido):
            prestamo = Prestamo(libro, usuario)
    
    def test_registrar_devolucion(self):
        """Verifica que se puede registrar una devolución."""
        libro = Libro("Título", "Autor", "ISBN", 2008, 100)
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        prestamo = Prestamo(libro, usuario)
        
        multa = prestamo.registrar_devolucion()
        assert prestamo.estado == "devuelto"
        assert libro.disponible is True


class TestBiblioteca:
    """Pruebas para la clase Biblioteca."""
    
    def setup_method(self):
        """Prepara datos para cada prueba."""
        MetaclaseSingleton._instancias.clear()
        self.biblioteca = Biblioteca("Test")
        self.usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        self.libro = Libro("Título", "Autor", "ISBN", 2008, 100)
    
    def test_agregar_libro(self):
        """Verifica que se puede agregar un libro."""
        self.biblioteca.agregar_libro(self.libro)
        assert self.libro.isbn in self.biblioteca.libros
    
    def test_agregar_libro_duplicado_error(self):
        """Verifica error al agregar libro duplicado."""
        self.biblioteca.agregar_libro(self.libro)
        with pytest.raises(ValueError):
            self.biblioteca.agregar_libro(self.libro)
    
    def test_registrar_usuario(self):
        """Verifica que se puede registrar un usuario."""
        self.biblioteca.registrar_usuario(self.usuario)
        assert self.usuario.dni in self.biblioteca.usuarios
    
    def test_registrar_prestamo(self):
        """Verifica que se puede registrar un préstamo."""
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.registrar_usuario(self.usuario)
        
        prestamo = self.biblioteca.registrar_prestamo(self.usuario.dni, self.libro.isbn)
        assert prestamo.id_prestamo in self.biblioteca.prestamos
    
    def test_registrar_prestamo_libro_no_disponible_error(self):
        """Verifica error al prestar libro no disponible."""
        usuario2 = Usuario("María", "García", "87654321", "maria@email.com")
        
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.registrar_usuario(self.usuario)
        self.biblioteca.registrar_usuario(usuario2)
        
        self.biblioteca.registrar_prestamo(self.usuario.dni, self.libro.isbn)
        
        with pytest.raises(LibroNoDisponible):
            self.biblioteca.registrar_prestamo(usuario2.dni, self.libro.isbn)
    
    def test_registrar_devolucion(self):
        """Verifica que se puede registrar una devolución."""
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.registrar_usuario(self.usuario)
        
        prestamo = self.biblioteca.registrar_prestamo(self.usuario.dni, self.libro.isbn)
        multa = self.biblioteca.registrar_devolucion(prestamo.id_prestamo)
        
        assert prestamo.id_prestamo not in self.biblioteca.prestamos
    
    def test_listar_libros_disponibles(self):
        """Verifica que se listan solo libros disponibles."""
        libro2 = Libro("Otro", "Autor", "ISBN2", 2008, 100)
        
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.agregar_libro(libro2)
        self.biblioteca.registrar_usuario(self.usuario)
        
        self.biblioteca.registrar_prestamo(self.usuario.dni, self.libro.isbn)
        
        disponibles = self.biblioteca.listar_libros_disponibles()
        assert len(disponibles) == 1
        assert disponibles[0].isbn == "ISBN2"
    
    def test_obtener_estadisticas(self):
        """Verifica que se obtienen estadísticas correctas."""
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.registrar_usuario(self.usuario)
        
        stats = self.biblioteca.obtener_estadisticas()
        assert stats["total_libros"] == 1
        assert stats["total_usuarios"] == 1


class TestHerencia:
    """Pruebas para verificar herencia correcta."""
    
    def test_usuario_es_instancia_persona(self):
        """Verifica que Usuario hereda de Persona."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        assert isinstance(usuario, Persona)
    
    def test_bibliotecario_es_instancia_persona(self):
        """Verifica que Bibliotecario hereda de Persona."""
        bib = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com")
        assert isinstance(bib, Persona)


class TestPolimorfismo:
    """Pruebas para verificar polimorfismo."""
    
    def test_polimorfismo_str(self):
        """Verifica que __str__() es diferente en cada clase."""
        usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
        bib = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com")
        
        str_usuario = str(usuario)
        str_bib = str(bib)
        
        assert "Usuario" in str_usuario
        assert "Bibliotecario" in str_bib
        assert str_usuario != str_bib


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
