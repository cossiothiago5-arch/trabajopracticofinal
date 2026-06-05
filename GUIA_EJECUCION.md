# 🚀 GUÍA DE EJECUCIÓN - Sistema de Gestión de Biblioteca Digital

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes)
- **git** (para clonar el repositorio)

## ⚙️ Instalación y Configuración

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/cossiothiago5-arch/trabajopracticofinal.git
cd trabajopracticofinal
```

### Paso 2: Crear entorno virtual (recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Ejecutar la Aplicación

### Opción 1: Ejecutar demostración completa

```bash
python src/main.py
```

Esta opción ejecuta una demostración completa que muestra:
- ✅ Patrón Singleton en acción
- ✅ Herencia y Polimorfismo
- ✅ Agregación y Composición
- ✅ Decoradores personalizados
- ✅ Metaclase funcionando
- ✅ Manejo de errores
- ✅ Estadísticas del sistema

### Opción 2: Ejecutar pruebas unitarias

```bash
python -m pytest tests/ -v
```

Ejecuta todas las pruebas unitarias del sistema con reporte detallado.

**Con cobertura de código:**
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 📚 Uso Manual en Python

```python
from src.patrones import Biblioteca
from src.personas import Usuario
from src.libros import Libro

# Obtener instancia única de la biblioteca (Singleton)
biblioteca = Biblioteca.obtener_instancia()

# Crear usuario
usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
biblioteca.registrar_usuario(usuario)

# Crear libro
libro = Libro("Clean Code", "Robert C. Martin", "978-0132350884", 2008, 464)
biblioteca.agregar_libro(libro)

# Realizar préstamo
prestamo = biblioteca.registrar_prestamo(usuario.dni, libro.isbn)
print(prestamo)

# Listar libros disponibles
for libro_disponible in biblioteca.listar_libros_disponibles():
    print(libro_disponible)

# Devolver libro
multa = biblioteca.registrar_devolucion(prestamo.id_prestamo)
print(f"Multa por retraso: ${multa:.2f}")

# Ver estadísticas
print(biblioteca.obtener_estadisticas())
```

## 📁 Estructura de Archivos

```
trabajopracticofinal/
├── README.md                 # Descripción general del proyecto
├── GUIA_EJECUCION.md        # Este archivo
├── requirements.txt          # Dependencias del proyecto
├── diagrama_uml.md          # Diagrama UML del sistema
├── src/
│   ├── __init__.py          # Inicializador del paquete
│   ├── main.py              # Punto de entrada (demostración)
│   ├── personas.py          # Clases Persona, Usuario, Bibliotecario
│   ├── libros.py            # Clase Libro
│   ├── prestamos.py         # Clase Préstamo (composición)
│   ├── patrones.py          # Clase Biblioteca (Singleton)
│   ├── decoradores.py       # Decoradores personalizados
│   ├── metaclases.py        # MetaclaseSingleton
│   └── excepciones.py       # Excepciones personalizadas
└── tests/
    ├── __init__.py          # Inicializador del paquete de tests
    └── test_sistema.py      # Pruebas unitarias
```

## 🧪 Ejemplos de Uso

### Crear usuarios y libros

```python
from src.personas import Usuario, Bibliotecario
from src.libros import Libro
from src.patrones import Biblioteca

# Crear instancia de la biblioteca (Singleton)
biblioteca = Biblioteca("Mi Biblioteca")

# Crear usuarios
usuario1 = Usuario("Juan", "Pérez", "12345678", "juan@example.com")
usuario2 = Usuario("María", "García", "87654321", "maria@example.com")

# Crear bibliotecario
bibliotecario = Bibliotecario("Carlos", "López", "11111111", "carlos@example.com", "administrador")

# Registrar en la biblioteca
biblioteca.registrar_usuario(usuario1)
biblioteca.registrar_usuario(usuario2)
biblioteca.registrar_usuario(bibliotecario)

# Crear libros
libro1 = Libro("Clean Code", "Robert C. Martin", "978-0132350884", 2008, 464)
libro2 = Libro("Design Patterns", "Gang of Four", "978-0201633610", 1994, 395)

# Agregar libros a la biblioteca
biblioteca.agregar_libro(libro1)
biblioteca.agregar_libro(libro2)
```

### Realizar préstamos y devoluciones

```python
# Realizar préstamo
prestamo1 = biblioteca.registrar_prestamo(usuario1.dni, libro1.isbn)
print(f"Préstamo realizado: {prestamo1.id_prestamo}")

# Ver préstamos activos del usuario
prestamos_activos = biblioteca.obtener_prestamos_activos(usuario1.dni)
for p in prestamos_activos:
    print(f"- {p.libro.titulo} (vence: {p.fecha_devolucion_esperada.strftime('%d/%m/%Y')})")

# Devolver libro
multa = biblioteca.registrar_devolucion(prestamo1.id_prestamo)
if multa > 0:
    print(f"⚠️ Multa por retraso: ${multa:.2f}")
else:
    print("✓ Devolución realizada sin multa")
```

### Buscar libros

```python
# Buscar por ISBN
libro = biblioteca.buscar_libro_por_isbn("978-0132350884")
if libro:
    print(f"Encontrado: {libro.titulo}")

# Buscar por título (búsqueda parcial)
resultados = biblioteca.buscar_libro_por_titulo("Clean")
for libro in resultados:
    print(f"- {libro.titulo}")

# Listar libros disponibles
disponibles = biblioteca.listar_libros_disponibles()
print(f"Libros disponibles: {len(disponibles)}")
```

### Obtener estadísticas

```python
# Ver estadísticas del sistema
stats = biblioteca.obtener_estadisticas()

print(f"Total de libros: {stats['total_libros']}")
print(f"Libros disponibles: {stats['libros_disponibles']}")
print(f"Libros prestados: {stats['libros_prestados']}")
print(f"Total de usuarios: {stats['total_usuarios']}")
print(f"Préstamos activos: {stats['prestamos_activos']}")
print(f"Préstamos retrasados: {stats['prestamos_retrasados']}")
```

## 🔍 Verificar Requisitos Técnicos

### 1. Herencia
```python
from src.personas import Persona, Usuario
usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
print(isinstance(usuario, Persona))  # True
```

### 2. Polimorfismo
```python
usuario = Usuario("Juan", "Pérez", "12345678", "juan@email.com")
bibliotecario = Bibliotecario("Carlos", "López", "99999999", "carlos@email.com")
print(str(usuario))        # Diferente formato
print(str(bibliotecario))  # Diferente formato
```

### 3. Agregación
```python
# La Biblioteca contiene Libros y Usuarios
biblioteca = Biblioteca()
biblioteca.agregar_libro(libro)
biblioteca.registrar_usuario(usuario)
# Los elementos pueden existir independientemente
```

### 4. Composición
```python
# Un Préstamo está compuesto por Libro y Usuario
prestamo = Prestamo(libro, usuario)
# Sin Libro y Usuario, el Préstamo no tiene sentido
```

### 5. Decorador
```python
# @registrar_operacion registra automáticamente operaciones
biblioteca.registrar_prestamo(usuario.dni, libro.isbn)
# Se imprime en consola información de la operación
```

### 6. Metaclase
```python
from src.metaclases import MetaclaseSingleton
# La metaclase controla la instancia única de Biblioteca
bib1 = Biblioteca()
bib2 = Biblioteca()
print(bib1 is bib2)  # True (Singleton)
```

### 7. Patrón Singleton
```python
# El patrón Singleton garantiza una única instancia
biblioteca = Biblioteca.obtener_instancia()
# Todos acceden a la misma instancia
```

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'src'"

**Solución:** Asegúrate de estar ejecutando desde el directorio raíz del proyecto:
```bash
cd trabajopracticofinal
python src/main.py
```

### Error: "No module named 'pytest'"

**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Los tests no se ejecutan

**Solución:** Asegúrate de que pytest esté instalado:
```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

## 📞 Información de Contacto

**Integrantes del grupo:**
- Bustos, Lisandros
- Cossio, Benjamin
- González, Enzo
- Franco, Palacios

## 📅 Fecha de Entrega
Junio de 2026

---

**Última actualización:** 2026-06-05
