# Date Clean

Date Clean es un paquete de Python diseñado para simplificar el trabajo con fechas en el análisis de datos. Homogeniza fechas de diversos formatos, incluyendo formatos populares encontrados en sitios web como WordPress, Joomla y otros, a un formato estándar. Esto facilita el procesamiento y análisis de datos que contienen fechas en diferentes formatos.

## Instalación

Puedes instalar el paquete usando pip:

```bash
pip install git+https://github.com/gerickt/date_clean.git
```

## Uso
La función principal del paquete es `homogenize_date(date_string, include_time=Bool, timezone)`. Esta función toma una cadena de texto (fecha) como entrada y devuelve una fecha formateada en el formato ISO 8601. 

**Parámetro obligatorio `include_time`:**
La función `homogenize_date` tiene el parametro obligatorio `include_time` (por defecto en `True`). Si se establece en `True`, incluira en la salida la hora y zona horaria: YYYY-MM-DDTHH:MM:SS-TZ o YYYY-MM-DD si es `False`.

**Parámetro opcional `assume_current_century`:**

La función `homogenize_date` ahora tiene un parámetro opcional `assume_current_century` (por defecto en `True`). Si se establece en `True`, la librería asumirá que los años abreviados (por ejemplo, "24") pertenecen al siglo actual. Puedes cambiarlo a `False` si necesitas interpretar los años abreviados de otra manera.

**Ejemplo de uso:**
```python
import date_clean as dc

date_str = "1 hora"
formatted_date = dc.homogenize_date(date_str, include_time=True, timezone="America/La_Paz")
print(formatted_date)  # Output (fecha y hora actual - 1 hora en formato ISO 8601): 2024-08-04T04:30:00-04:00

date_century = "05/Agosto/24"

# Asumir siglo actual (2024)
formatted_date = dc.homogenize_date(date_century, include_time=True, timezone="America/La_Paz")
print(formatted_date)  # Output: 2024-08-05T...

# No asumir siglo actual (1924)
formatted_date = dc.homogenize_date(date_century, include_time=True, timezone="America/La_Paz", assume_current_century=False)
print(formatted_date)  # Output: 1924-08-05T...
```

**Manejo de diversos formatos:**

Date Clean puede manejar una variedad de formatos de fecha, incluyendo:
- Relativos: "hace 1 hora", "hace 2 días"
- WordPress: "agosto 5, 2024", "5 de agosto de 2024"
- Joomla: "05/08/2024", "2024-08-05"
- Otros formatos populares: "05.08.2024", "5 Ago 2024", "Lunes, 5 de Agosto de 2024"

**Ejemplo con diferentes formatos:**
```python
import date_clean as dc

date_formats = [
    "1 hora",
    "05-08-2024 18:00",
    "05 Agosto 2024",
    "5 agosto, 2024",
    "sabado, 3 de agosto de 2024, 11:00",
    # ... más formatos
]

for date_str in date_formats:
    formatted_date = dc.homogenize_date(date_str, include_time=True, timezone="America/La_Paz")
    print(f"Formato original: {date_str}, Formato homogenizado: {formatted_date}")
```

**Beneficios de usar Date Clean:**
- Facilidad de uso: Una simple función para manejar múltiples formatos de fecha.
- Consistencia: Asegura que todas las fechas estén en un formato estándar.
- Eficiencia: Reduce el tiempo y esfuerzo necesarios para limpiar y preparar datos de fechas.

**Contribuciones:**

Las contribuciones son bienvenidas! Si encuentras un formato de fecha que no es manejado correctamente, por favor crea un issue o un pull request.