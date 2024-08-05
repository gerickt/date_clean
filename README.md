# Date Clean

Date Clean es un paquete para homogenizar fechas de diferentes formatos en un formato específico.

## Instalación

Puedes instalar el paquete usando pip:

```bash
pip install git+https://github.com/gerickt/date_clean.git
```

## Uso
Ejemplo de uso del paquete:

```python
import date_clean as dc

date_str = "1 hora"
formatted_date = dc.homogenize_date(date_str, include_time=True, timezone="America/La_Paz")
print(formatted_date)  # Output: "05/08/2024 15:00"
```
