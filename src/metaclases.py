"""
Módulo de metaclases para el sistema de gestión de biblioteca digital.

Este módulo implementa la metaclase Singleton para garantizar una única
instancia de la clase Biblioteca en toda la aplicación.
"""

from typing import Any, Dict


class MetaclaseSingleton(type):
    """
    Metaclase que implementa el patrón Singleton.
    
    Garantiza que solo exista una única instancia de la clase que use
    esta metaclase. La instancia se crea la primera vez que se accede
    a la clase y se reutiliza en todos los accesos posteriores.
    
    Ejemplo:
        class Biblioteca(metaclass=MetaclaseSingleton):
            pass
        
        b1 = Biblioteca()
        b2 = Biblioteca()
        assert b1 is b2  # Misma instancia
    """
    
    _instancias: Dict[type, Any] = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Sobrescribe el método __call__ para controlar la creación de instancias.
        
        Si la clase ya tiene una instancia almacenada, la devuelve.
        Si no, crea una nueva instancia, la almacena y la devuelve.
        
        Args:
            *args: Argumentos posicionales para el constructor
            **kwargs: Argumentos nombrados para el constructor
            
        Returns:
            La única instancia de la clase
        """
        if cls not in cls._instancias:
            # Crear nueva instancia si no existe
            instancia = super(MetaclaseSingleton, cls).__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
            print(f"[METACLASE] Nueva instancia de {cls.__name__} creada (Singleton)")
        else:
            print(f"[METACLASE] Devolviendo instancia existente de {cls.__name__}")
        
        return cls._instancias[cls]
    
    @classmethod
    def resetear_instancias(mcs):
        """
        Método para resetear todas las instancias almacenadas.
        Útil para pruebas unitarias.
        """
        mcs._instancias.clear()
        print("[METACLASE] Todas las instancias han sido reseteadas")
