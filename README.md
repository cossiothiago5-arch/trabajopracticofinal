# Sistema de Gestión de Biblioteca Digital

## 📚 Descripción del Sistema

Sistema integral para la administración de una biblioteca digital desarrollado en Python utilizando Programación Orientada a Objetos. Permite gestionar libros, usuarios y préstamos con validaciones robustas y patrones de diseño profesionales.

### Características principales:
- ✅ **Gestión de Libros**: Alta, modificación, baja y listado de libros con metadatos completos
- ✅ **Gestión de Usuarios**: Registro y administración de usuarios de la biblioteca
- ✅ **Sistema de Préstamos**: Control de préstamos y devoluciones con validaciones
- ✅ **Arquitectura OOP**: Herencia, polimorfismo, agregación y composición
- ✅ **Patrones de Diseño**: Implementación del patrón Singleton
- ✅ **Decoradores Personalizados**: Validación y logging de operaciones
- ✅ **Metaclases**: Control avanzado de instancias

## 👥 Integrantes del Grupo

1. **Bustos, Lisandros**
2. **Cossio, Benjamin**
3. **González, Enzo**
4. **Franco, Palacios**

## 🚀 Instrucciones de Ejecución

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/cossiothiago5-arch/trabajopracticofinal.git
   cd trabajopracticofinal
   ```

2. **Crear un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python src/main.py
   ```

### Estructura del Proyecto

```
trabajopracticofinal/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias del proyecto
├── diagrama_uml.md          # Diagrama UML del sistema
├── src/
│   ├── __init__.py          # Inicializador del paquete
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── personas.py          # Jerarquía de herencia: Persona → Usuario/Bibliotecario
│   ├── libros.py            # Gestión de libros
│   ├── prestamos.py         # Gestión de préstamos
│   ├── decoradores.py       # Decoradores personalizados
│   ├── metaclases.py        # Metaclases (Singleton)
│   ├── patrones.py          # Patrón Singleton para Biblioteca
│   └── excepciones.py       # Excepciones personalizadas
└── tests/
    └── test_sistema.py      # Pruebas unitarias
```

## 🏗️ Requisitos Técnicos Implementados

### 1. **Herencia**
- Clase base `Persona` con atributos comunes
- Clases derivadas `Usuario` y `Bibliotecario` con comportamientos específicos

### 2. **Polimorfismo**
- Método `__str__()` implementado en múltiples clases
- Método `calcular_multa()` con diferentes implementaciones

### 3. **Agregación**
- Clase `Biblioteca` contiene colecciones de `Libros` y `Usuarios`
- Relación "es-parte-de" débil: los elementos pueden existir independientemente

### 4. **Composición**
- Clase `Préstamo` compuesta por `Libro` y `Usuario`
- Relación fuerte: no tiene sentido sin sus componentes

### 5. **Decorador Personalizado**
- `@validar_datos`: Valida tipos de datos antes de asignar valores
- `@registrar_operacion`: Registra todas las operaciones del sistema

### 6. **Metaclase**
- `MetaclaseSingleton`: Implementa el patrón Singleton para garantizar una única instancia de Biblioteca

### 7. **Patrón de Diseño**
- **Patrón Singleton**: Asegura una única instancia central de la Biblioteca en todo el sistema

## 📖 Ejemplo de Uso

```python
from src.patrones import Biblioteca
from src.personas import Usuario
from src.libros import Libro

# Obtener instancia única de la biblioteca (Singleton)
biblioteca = Biblioteca.obtener_instancia()

# Crear un usuario
usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
biblioteca.registrar_usuario(usuario)

# Crear un libro
libro = Libro("Clean Code", "Robert C. Martin", "978-0132350884", 2008, 464)
biblioteca.agregar_libro(libro)

# Realizar préstamo
biblioteca.registrar_prestamo(usuario.dni, libro.isbn)

# Listar libros disponibles
biblioteca.listar_libros_disponibles()
```

## 🧪 Pruebas

Ejecutar las pruebas unitarias:
```bash
python -m pytest tests/ -v
```

## 📝 Notas de Desarrollo

- Todos los métodos incluyen validaciones robustas
- Se implementaron excepciones personalizadas para manejo de errores
- El código sigue las convenciones PEP 8
- Cada clase tiene documentación mediante docstrings

## 📅 Fecha de Entrega
Junio de 2026

---

**Desarrollado como trabajo práctico final de Programación Orientada a Objetos**
