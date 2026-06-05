"""
Módulo de libros del sistema de gestión de biblioteca digital.

Define la clase Libro que representa un libro en el sistema de la biblioteca.
"""

from datetime import datetime


class Libro:
    """
    Clase que representa un libro en la biblioteca.
    
    Un libro contiene información sobre su contenido y está disponible
    para ser prestado a los usuarios.
    
    Attributes:
        titulo (str): Título del libro
        autor (str): Autor del libro
        isbn (str): ISBN único del libro
        anio_publicacion (int): Año de publicación
        cantidad_paginas (int): Cantidad de páginas
        disponible (bool): Indica si el libro está disponible
        fecha_registro (datetime): Fecha de registro en el sistema
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str, 
                 anio_publicacion: int, cantidad_paginas: int):
        """
        Inicializa un nuevo libro.
        
        Args:
            titulo: Título del libro
            autor: Autor del libro
            isbn: ISBN del libro (único)
            anio_publicacion: Año de publicación
            cantidad_paginas: Cantidad de páginas
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        self._validar_datos(titulo, autor, isbn, anio_publicacion, cantidad_paginas)
        
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio_publicacion = anio_publicacion
        self.cantidad_paginas = cantidad_paginas
        self.disponible = True
        self.fecha_registro = datetime.now()
        self.prestamo_activo = None  # ID del préstamo activo
    
    @staticmethod
    def _validar_datos(titulo: str, autor: str, isbn: str, 
                       anio_publicacion: int, cantidad_paginas: int):
        """
        Valida los datos del libro.
        
        Args:
            titulo: Título del libro
            autor: Autor del libro
            isbn: ISBN del libro
            anio_publicacion: Año de publicación
            cantidad_paginas: Cantidad de páginas
            
        Raises:
            ValueError: Si algún dato es inválido
        """
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        
        if not autor or len(autor.strip()) == 0:
            raise ValueError("El autor no puede estar vacío")
        
        if not isbn or len(isbn.strip()) == 0:
            raise ValueError("El ISBN no puede estar vacío")
        
        if not isinstance(anio_publicacion, int) or anio_publicacion < 1000:
            raise ValueError("El año de publicación debe ser un número válido")
        
        if not isinstance(cantidad_paginas, int) or cantidad_paginas <= 0:
            raise ValueError("La cantidad de páginas debe ser un número positivo")
    
    def marcar_como_prestado(self, prestamo_id: str):
        """
        Marca el libro como prestado.
        
        Args:
            prestamo_id: ID del préstamo
        """
        self.disponible = False
        self.prestamo_activo = prestamo_id
    
    def marcar_como_disponible(self):
        """Marca el libro como disponible nuevamente."""
        self.disponible = True
        self.prestamo_activo = None
    
    def obtener_edad(self) -> int:
        """
        Calcula la edad del libro (años desde su publicación).
        
        Returns:
            int: Edad del libro en años
        """
        return datetime.now().year - self.anio_publicacion
    
    def __str__(self) -> str:
        """Representación en string del libro."""
        estado = "Disponible" if self.disponible else "Prestado"
        return (f"📚 {self.titulo} | Autor: {self.autor} | "
                f"ISBN: {self.isbn} | Año: {self.anio_publicacion} | "
                f"Páginas: {self.cantidad_paginas} | Estado: {estado}")
    
    def __repr__(self) -> str:
        """Representación técnica del libro."""
        return f"Libro({self.titulo}, {self.autor}, {self.isbn})"
    
    def __eq__(self, otro) -> bool:
        """Compara libros por ISBN."""
        if not isinstance(otro, Libro):
            return False
        return self.isbn == otro.isbn
    
    def __hash__(self) -> int:
        """Permite usar objetos Libro en sets y dicts."""
        return hash(self.isbn)
    
    def __lt__(self, otro) -> bool:
        """Compara libros por título para ordenamiento."""
        if not isinstance(otro, Libro):
            return NotImplemented
        return self.titulo.lower() < otro.titulo.lower()
    
    def obtener_info_completa(self) -> dict:
        """
        Retorna un diccionario con la información completa del libro.
        
        Returns:
            dict: Información del libro
        """
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "anio_publicacion": self.anio_publicacion,
            "cantidad_paginas": self.cantidad_paginas,
            "disponible": self.disponible,
            "edad": self.obtener_edad(),
            "fecha_registro": self.fecha_registro.isoformat(),
            "prestamo_activo": self.prestamo_activo
        }
