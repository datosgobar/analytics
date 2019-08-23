# Herramientas auxiliares

## Descarga de CSVs

1) Obtener una cookie para API Management.

2) Con un entorno virtual de Python activado:

Instalar las dependencias:
```bash
$ pip3 install -r requirements.txt
```

Invocar el script:
```bash
$ python3 download.py --api <nombre> --cookie <cookie> --output <carpeta> --from-date <date>
```

El formato de `date` debe seguir el estilo YYYY-MM-DD. Opcionalmente, se puede utilizar el parámetro `--end-date` para modificar el límite superior del intervalo de descargas.

Ejemplos:

```bash
$ python3 download.py --api series-tiempo-prod --cookie 'xyz' --output datos --from-date 2018-01-01
```

```bash
$ python3 download.py --api georef-prod --cookie 'xyz' --output datos --from-date 2018-02-03 --end-date 2018-06-10
```

### Makefile para descarga de CSV's

Se incluye un makefile con la receta *download*. Si no se indica el parámetro `OUTPUT_DIR`, por defecto, se descargan los archivos en `~/sdt-analytics-download`.

Ejemplo:
```bash
$ make download COOKIE='xyz' FROM_DATE='2018-01-01'
```

## Leer CSVs a un DataFrame

Importar o copiar la función del módulo para leer todos los CSVs del directorio de descarga de analytics a un mismo DataFrame.

```python
from download import read_files_to_df

df = read_files_to_df("/Users/abenassi/github/analytics/tools/datos/georef")
```
