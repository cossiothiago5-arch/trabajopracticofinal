"""
Excepciones personalizadas del sistema de gestión de biblioteca digital.
"""


class ErrorBiblioteca(Exception):
    """Excepción base para el sistema de biblioteca."""
    pass


class LibroNoEncontrado(ErrorBiblioteca):
    """Se lanza cuando un libro solicitado no existe."""
    pass


class UsuarioNoEncontrado(ErrorBiblioteca):
    """Se lanza cuando un usuario solicitado no existe."""
    pass


class PrestamoNoValido(ErrorBiblioteca):
    """Se lanza cuando se intenta un préstamo inválido."""
    pass


class DatosInvalidos(ErrorBiblioteca):
    """Se lanza cuando los datos ingresados no son válidos."""
    pass


class LibroNoDisponible(ErrorBiblioteca):
    """Se lanza cuando se intenta prestar un libro no disponible."""
    pass


class DevolucioNoEncontrada(ErrorBiblioteca):
    """Se lanza cuando se intenta devolver un préstamo inexistente."""
    pass
