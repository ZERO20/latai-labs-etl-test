# 🚀 ETL Users Project

Proceso ETL en Python que extrae datos de usuarios desde la API de JSONPlaceholder, los transforma aplicando validaciones y normalizaciones, y los carga en un archivo CSV.

> 🧪 Este proyecto fue desarrollado como parte de una **prueba técnica para Latai Labs**.


## 📋 Descripción

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) que:

1. **Extrae** datos de usuarios desde [JSONPlaceholder API](https://jsonplaceholder.typicode.com/users)
2. **Transforma** los datos aplicando:
   - Validación de emails (eliminando registros con emails inválidos)
   - Normalización de nombres (conversión a mayúsculas)
   - Creación de direcciones completas (uniendo street, suite, city, zipcode)
   - Eliminación de IDs duplicados
3. **Carga** los datos procesados en `output/users_cleaned.csv`

## 🏗️ Estructura del Proyecto

```
latai-labs-etl-test/
├── etl/
│   ├── __init__.py          # Módulo principal ETL
│   ├── extract.py           # Extracción de datos
│   ├── transform.py         # Transformaciones
│   └── load.py              # Carga a CSV
├── tests/
│   ├── __init__.py          # Paquete de tests
│   ├── test_extract.py      # Tests de extracción
│   ├── test_load.py         # Tests de carga
│   └── test_transform.py    # Tests de transformación
├── output/
│   └── users_cleaned.csv    # Archivo de salida (generado)
├── main.py                  # Script principal
├── requirements.txt         # Dependencias
├── etl_process.log          # Log del proceso (generado)
└── README.md                # Documentación
```

## 🛠️ Requisitos del Sistema

### **Environment de Desarrollo**
- **Python**: 3.12.3 (versión utilizada en desarrollo)
- **Acceso a internet**: Para conexión a la API JSONPlaceholder

## 📦 Instalación

### **Opción 1: Usando Makefile (Recomendado)**
```bash
# Clonar repositorio
git clone https://github.com/ZERO20/latai-labs-etl-test.git
cd latai-labs-etl-test

# Instalar dependencias
make install
```

### **Opción 2: Manual**
```bash
# Clonar repositorio
git clone https://github.com/ZERO20/latai-labs-etl-test.git
cd latai-labs-etl-test

# Instalar dependencias
pip install -r requirements.txt
```

### **Opción 3: Con Virtual Environment**
```bash
# Crear environment virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

### **Usando Makefile (Recomendado)**
```bash
# Ejecutar proceso ETL completo
make run

# Ejecutar todos los tests
make test

# Ejecutar pruebas con coverage
make coverage

# Ejecutar pruebas con coverage y ver reporte en navegador
make coverage-open

# Formatear código con Black
make format

# Verificar calidad del código con Flake8
make lint

# Limpiar archivos generados
make clean

# Ver todos los comandos disponibles
make help
```

### **Ejecución Manual**
```bash
# Ejecutar el proceso ETL completo
python main.py

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar coverage completo
pytest tests/ --cov=etl --cov-report=term-missing

# Ejecutar tests individuales
pytest tests/test_extract.py
pytest tests/test_transform.py
pytest tests/test_load.py
```

## 📊 Salida

El proceso genera:
- **`output/users_cleaned.csv`**: Archivo CSV con los datos procesados
- **`etl_process.log`**: Log del proceso ETL

### Formato del CSV de salida

| Campo | Descripción |
|-------|-------------|
| `id` | ID único del usuario |
| `name` | Nombre en mayúsculas |
| `email` | Email válido |
| `full_address` | Dirección completa (street, suite, city, zipcode) |

## 🧪 Testing

Las pruebas cubren:
### Extraer (`test_extract.py`)
- ✅ Extracción exitosa de datos de usuarios desde API
- ✅ Manejo de respuestas vacías
- ✅ Errores de conexión (timeout, connection error, request exception)
- ✅ Errores HTTP (404, 500)
- ✅ Respuestas con JSON inválido
- ✅ Validación de formato de respuesta (debe ser lista)

### Transformaciones (`test_transform.py`)
- ✅ Validación de emails (válidos e inválidos)
- ✅ Normalización de nombres
- ✅ Formateo de direcciones completas
- ✅ Eliminación de duplicados por ID
- ✅ Flujo completo de transformación

### Carga de datos (`test_load.py`)
- ✅ Creación correcta de archivos CSV
- ✅ Validación de estructura de archivos
- ✅ Manejo de directorios de salida
- ✅ Manejo de errores


## 📝 Logging

El proceso incluye logging completo que registra:
- Inicio y fin del proceso ETL
- Número de usuarios extraídos
- Usuarios filtrados por email inválido
- Duplicados eliminados
- Errores y excepciones
- Validación del archivo de salida

## 🚨 Manejo de Errores
- Errores de conexión a la API
- Timeouts de requests
- Datos malformados
- Problemas de escritura de archivos
- Validaciones de email


## 📋 TODO
- Añadir lógica de reintento con backoff exponencial para manejar errores de requests.