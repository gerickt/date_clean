# Date Clean

Date Clean es un paquete de Python diseñado para simplificar el trabajo con fechas en el análisis de datos. Homogeniza fechas de diversos formatos, incluyendo formatos populares encontrados en sitios web como WordPress, Joomla y otros, a un formato estándar. Esto facilita el procesamiento y análisis de datos que contienen fechas en diferentes formatos.

## Instalación

Puedes instalar el paquete usando pip:

```bash
pip install git+https://github.com/gerickt/date_clean.git
```

## Uso
La función principal del paquete es homogenize_date(date_str, include_time=False, timezone="UTC"). Esta función toma una cadena de fecha como entrada y devuelve una fecha formateada en el formato YYYY-MM-DDTHH:MM:SS-TZ si include_time es True, o YYYY-MM-DD si es False.

**Ejemplo de uso:**
```python
import date_clean as dc

date_str = "1 hora"
formatted_date = dc.homogenize_date(date_str, include_time=True, timezone="America/La_Paz")
print(formatted_date)  # Output (fecha y hora actual - 1 hora en formato ISO 8601): 2024-08-04T04:30:00-04:00
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