"""
Módulo de personas del sistema de gestión de biblioteca digital.

Define la jerarquía de herencia con la clase base Persona y sus derivadas.
Implementa polimorfismo mediante métodos que se sobrescriben en las clases
derivadas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from src.decoradores import validar_datos, validar_email


class Persona(ABC):
    """
    Clase abstracta que representa una persona en el sistema.
    
    Esta es la clase base de la jerarquía de herencia. Define atributos
    y métodos comunes a todas las personas del sistema.
    
    Attributes:
        nombre (str): Nombre de la persona
        apellido (str): Apellido de la persona
        dni (str): Documento Nacional de Identidad
        email (str): Correo electrónico de la persona
    """
    
    def __init__(self, nombre: str, apellido: str, dni: str, email: str):
        """
        Inicializa una nueva persona.
        
        Args:
            nombre: Nombre de la persona
            apellido: Apellido de la persona
            dni: DNI de la persona
            email: Correo electrónico
        """
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.fecha_registro = datetime.now()
    
    @abstractmethod
    def obtener_tipo(self) -> str:
        """Método abstracto que debe implementarse en subclases."""
        pass
    
    @abstractmethod
    def obtener_permisos(self) -> list:
        """Retorna los permisos disponibles para este tipo de persona."""
        pass
    
    def obtener_nombre_completo(self) -> str:
        """
        Retorna el nombre completo de la persona.
        
        Returns:
            str: Nombre y apellido concatenados
        """
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self) -> str:
        """
        Representación en string de la persona.
        Implementa polimorfismo.
        
        Returns:
            str: Información de la persona
        """
        return f"{self.obtener_tipo()}: {self.obtener_nombre_completo()} (DNI: {self.dni})"
    
    def __repr__(self) -> str:
        """Representación técnica de la persona."""
        return f"{self.__class__.__name__}({self.nombre}, {self.apellido}, {self.dni})"
    
    def __eq__(self, otro) -> bool:
        """Compara personas por DNI."""
        if not isinstance(otro, Persona):
            return False
        return self.dni == otro.dni
    
    def __hash__(self) -> int:
        """Permite usar objetos Persona en sets y dicts."""
        return hash(self.dni)


class Usuario(Persona):
    """
    Clase que representa un usuario de la biblioteca.
    
    Un usuario es una persona que puede realizar préstamos de libros.
    Hereda de la clase Persona.
    
    Attributes:
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        dni (str): DNI del usuario
        email (str): Correo del usuario
        estado (str): Estado del usuario ('activo' o 'inactivo')
        prestamos_activos (int): Cantidad de préstamos activos
    """
    
    def __init__(self, nombre: str, apellido: str, dni: str, email: str):
        """
        Inicializa un nuevo usuario.
        
        Args:
            nombre: Nombre del usuario
            apellido: Apellido del usuario
            dni: DNI del usuario
            email: Correo electrónico del usuario
        """
        super().__init__(nombre, apellido, dni, email)
        self.estado = "activo"
        self.prestamos_activos = 0
        self.multa_pendiente = 0.0
    
    def obtener_tipo(self) -> str:
        """Retorna el tipo de persona."""
        return "Usuario"
    
    def obtener_permisos(self) -> list:
        """
        Retorna los permisos de un usuario.
        
        Returns:
            list: Lista de permisos disponibles
        """
        return ["solicitar_prestamo", "devolver_libro", "ver_historial"]
    
    def puede_realizar_prestamo(self) -> bool:
        """
        Verifica si el usuario puede realizar un nuevo préstamo.
        
        Returns:
            bool: True si puede, False en caso contrario
        """
        return self.estado == "activo" and self.multa_pendiente == 0.0
    
    def incrementar_prestamos(self):
        """Incrementa el contador de préstamos activos."""
        self.prestamos_activos += 1
    
    def decrementar_prestamos(self):
        """Decrementa el contador de préstamos activos."""
        if self.prestamos_activos > 0:
            self.prestamos_activos -= 1
    
    def aplicar_multa(self, cantidad: float):
        """
        Aplica una multa al usuario.
        
        Args:
            cantidad: Cantidad de la multa
        """
        self.multa_pendiente += cantidad
    
    def pagar_multa(self, cantidad: float) -> bool:
        """
        Registra el pago de una multa.
        
        Args:
            cantidad: Cantidad a pagar
            
        Returns:
            bool: True si se pagó correctamente
        """
        if cantidad <= self.multa_pendiente:
            self.multa_pendiente -= cantidad
            return True
        return False
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        return (f"{super().__str__()} | Estado: {self.estado} | "
                f"Préstamos: {self.prestamos_activos} | Multa: ${self.multa_pendiente:.2f}")


class Bibliotecario(Persona):
    """
    Clase que representa un bibliotecario del sistema.
    
    Un bibliotecario es una persona con permisos adicionales para
    administrar libros y usuarios. Hereda de la clase Persona.
    
    Attributes:
        nombre (str): Nombre del bibliotecario
        apellido (str): Apellido del bibliotecario
        dni (str): DNI del bibliotecario
        email (str): Correo del bibliotecario
        numero_empleado (str): Número de empleado único
        nivel_acceso (str): Nivel de acceso ('basico', 'avanzado', 'administrador')
    """
    
    contador_empleados = 1000
    
    def __init__(self, nombre: str, apellido: str, dni: str, email: str, 
                 nivel_acceso: str = "basico"):
        """
        Inicializa un nuevo bibliotecario.
        
        Args:
            nombre: Nombre del bibliotecario
            apellido: Apellido del bibliotecario
            dni: DNI del bibliotecario
            email: Correo del bibliotecario
            nivel_acceso: Nivel de acceso (por defecto 'basico')
        """
        super().__init__(nombre, apellido, dni, email)
        Bibliotecario.contador_empleados += 1
        self.numero_empleado = f"BIB{Bibliotecario.contador_empleados}"
        self.nivel_acceso = nivel_acceso
        self.operaciones_realizadas = 0
    
    def obtener_tipo(self) -> str:
        """Retorna el tipo de persona."""
        return "Bibliotecario"
    
    def obtener_permisos(self) -> list:
        """
        Retorna los permisos de un bibliotecario.
        
        Returns:
            list: Lista de permisos disponibles
        """
        permisos_basicos = [
            "solicitar_prestamo",
            "devolver_libro",
            "ver_historial",
            "registrar_usuario",
            "agregar_libro"
        ]
        
        if self.nivel_acceso == "avanzado":
            permisos_basicos.extend([
                "modificar_usuario",
                "modificar_libro",
                "generar_reportes"
            ])
        
        if self.nivel_acceso == "administrador":
            permisos_basicos.extend([
                "eliminar_usuario",
                "eliminar_libro",
                "administrar_bibliotecarios",
                "configurar_sistema"
            ])
        
        return permisos_basicos
    
    def registrar_operacion(self):
        """Registra que el bibliotecario realizó una operación."""
        self.operaciones_realizadas += 1
    
    def tiene_permiso(self, permiso: str) -> bool:
        """
        Verifica si el bibliotecario tiene un permiso específico.
        
        Args:
            permiso: Nombre del permiso a verificar
            
        Returns:
            bool: True si tiene el permiso, False en caso contrario
        """
        return permiso in self.obtener_permisos()
    
    def __str__(self) -> str:
        """Representación en string del bibliotecario."""
        return (f"{super().__str__()} | Empleado: {self.numero_empleado} | "
                f"Acceso: {self.nivel_acceso} | Operaciones: {self.operaciones_realizadas}")
