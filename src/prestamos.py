"""
Módulo de préstamos del sistema de gestión de biblioteca digital.

Define la clase Préstamo que implementa la relación de composición
entre Libro y Usuario. Un préstamo no tiene sentido sin sus componentes.
"""

from datetime import datetime, timedelta
from src.libros import Libro
from src.personas import Usuario
from src.excepciones import PrestamoNoValido


class Prestamo:
    """
    Clase que representa un préstamo de un libro a un usuario.
    
    Implementa una relación de COMPOSICIÓN: el préstamo está compuesto
    por un Libro y un Usuario. Sin estos componentes, el préstamo no
    tiene razón de existir.
    
    Attributes:
        libro (Libro): El libro siendo prestado (composición)
        usuario (Usuario): El usuario que realiza el préstamo (composición)
        fecha_prestamo (datetime): Fecha en que se realizó el préstamo
        fecha_devolucion_esperada (datetime): Fecha esperada de devolución
        fecha_devolucion_real (datetime): Fecha real de devolución (None si no devuelto)
        estado (str): Estado del préstamo ('activo' o 'devuelto')
        id_prestamo (str): Identificador único del préstamo
    """
    
    contador_prestamos = 0
    DIAS_PRESTAMO = 14  # Duración estándar de un préstamo
    MULTA_POR_DIA_RETRASO = 5.0  # $ por día de retraso
    
    def __init__(self, libro: Libro, usuario: Usuario):
        """
        Inicializa un nuevo préstamo.
        
        Args:
            libro: El libro a prestar (composición)
            usuario: El usuario que realiza el préstamo (composición)
            
        Raises:
            PrestamoNoValido: Si el libro no está disponible o el usuario
                            no puede realizar préstamos
        """
        if not isinstance(libro, Libro):
            raise PrestamoNoValido("El libro debe ser una instancia de Libro")
        
        if not isinstance(usuario, Usuario):
            raise PrestamoNoValido("El usuario debe ser una instancia de Usuario")
        
        if not libro.disponible:
            raise PrestamoNoValido(f"El libro '{libro.titulo}' no está disponible")
        
        if not usuario.puede_realizar_prestamo():
            raise PrestamoNoValido(
                f"El usuario {usuario.obtener_nombre_completo()} no puede realizar préstamos"
            )
        
        # Relación de composición: el préstamo contiene el libro y el usuario
        self.libro = libro
        self.usuario = usuario
        
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion_esperada = self.fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)
        self.fecha_devolucion_real = None
        self.estado = "activo"
        
        # Generar ID único
        Prestamo.contador_prestamos += 1
        self.id_prestamo = f"PREST{Prestamo.contador_prestamos:06d}"
        
        # Actualizar estado del libro y usuario
        libro.marcar_como_prestado(self.id_prestamo)
        usuario.incrementar_prestamos()
    
    def calcular_dias_retraso(self) -> int:
        """
        Calcula los días de retraso (si aplica).
        
        Returns:
            int: Días de retraso, 0 si no hay retraso
        """
        if self.estado == "devuelto":
            dias_retraso = (self.fecha_devolucion_real - self.fecha_devolucion_esperada).days
            return max(0, dias_retraso)
        else:
            dias_retraso = (datetime.now() - self.fecha_devolucion_esperada).days
            return max(0, dias_retraso)
    
    def calcular_multa(self) -> float:
        """
        Calcula la multa por retraso (si aplica).
        
        Returns:
            float: Cantidad de multa a pagar
        """
        dias_retraso = self.calcular_dias_retraso()
        return dias_retraso * self.MULTA_POR_DIA_RETRASO
    
    def registrar_devolucion(self) -> float:
        """
        Registra la devolución del libro.
        
        Returns:
            float: Multa a pagar (0 si no hay retraso)
            
        Raises:
            PrestamoNoValido: Si el préstamo ya fue devuelto
        """
        if self.estado == "devuelto":
            raise PrestamoNoValido("Este préstamo ya fue devuelto")
        
        self.fecha_devolucion_real = datetime.now()
        self.estado = "devuelto"
        
        # Actualizar estado del libro y usuario
        self.libro.marcar_como_disponible()
        self.usuario.decrementar_prestamos()
        
        # Calcular multa si hay retraso
        multa = self.calcular_multa()
        if multa > 0:
            self.usuario.aplicar_multa(multa)
        
        return multa
    
    def esta_retrasado(self) -> bool:
        """
        Verifica si el préstamo está retrasado.
        
        Returns:
            bool: True si está retrasado, False en caso contrario
        """
        if self.estado == "devuelto":
            return self.fecha_devolucion_real > self.fecha_devolucion_esperada
        else:
            return datetime.now() > self.fecha_devolucion_esperada
    
    def obtener_dias_restantes(self) -> int:
        """
        Obtiene los días restantes para devolver el libro.
        
        Returns:
            int: Días restantes (negativo si está retrasado)
        """
        if self.estado == "devuelto":
            return 0
        
        dias_restantes = (self.fecha_devolucion_esperada - datetime.now()).days
        return dias_restantes
    
    def __str__(self) -> str:
        """Representación en string del préstamo."""
        return (f"Préstamo {self.id_prestamo} | Libro: {self.libro.titulo} | "
                f"Usuario: {self.usuario.obtener_nombre_completo()} | "
                f"Estado: {self.estado} | Fecha: {self.fecha_prestamo.strftime('%d/%m/%Y')}")
    
    def __repr__(self) -> str:
        """Representación técnica del préstamo."""
        return f"Prestamo({self.id_prestamo}, {self.libro.isbn}, {self.usuario.dni})"
    
    def obtener_info_completa(self) -> dict:
        """
        Retorna un diccionario con la información completa del préstamo.
        
        Returns:
            dict: Información del préstamo
        """
        return {
            "id_prestamo": self.id_prestamo,
            "libro": self.libro.titulo,
            "usuario": self.usuario.obtener_nombre_completo(),
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion_esperada": self.fecha_devolucion_esperada.isoformat(),
            "fecha_devolucion_real": self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
            "estado": self.estado,
            "retrasado": self.esta_retrasado(),
            "multa": self.calcular_multa()
        }
