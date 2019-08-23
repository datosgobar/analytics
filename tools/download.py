"""Herramienta para descargar CSVs con datos de consultas de API Management.
"""

import sys
import os
import requests
import click
from tqdm import tqdm
from datetime import datetime, date, timedelta


API_MANAGEMENT_URL = 'https://apis.datos.gob.ar'
DATE_FMT = '%Y-%m-%d'


def printerr(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
    exit(1)


def read_files_to_df(directory):
    """Lee CSVs de misma estructura en un directorio a un solo DataFrame."""

    file_pattern = os.path.join(directory, "*.csv")
    dfs = [pd.read_csv(file, encoding="utf8", parse_dates=True)
           for file in glob.glob(file_pattern)]

    return pd.concat(dfs, axis=0)


@click.command()
@click.option('--api', help='Nombre Kong de la API.', required=True)
@click.option('--cookie', help='Cookie de API Management.', required=True)
@click.option('--output', 'output_dir',
              help='Directorio de descarga (default: \'.\').', default='.',
              type=click.Path(exists=True, file_okay=False, writable=True))
@click.option('--from-date', help='Fecha de inicio (formato: YYYY-MM-DD).',
              required=True)
@click.option('--end-date',
              help='Fecha de final (formato: YYYY-MM-DD) (default: hoy).')
def download(api, cookie, output_dir, from_date, end_date):
    try:
        from_date = datetime.strptime(from_date, DATE_FMT).date()
    except ValueError:
        printerr('Error: Formato de from-date inválido.')

    if end_date:
        try:
            end_date = datetime.strptime(end_date, DATE_FMT).date()
        except ValueError:
            printerr('Error: Formato de end-date inválido.')
    else:
        end_date = date.today()

    if from_date > end_date:
        printerr('Error: from-date debe ser menor o igual a end-date.')

    print('Descargando archivos...')

    days = (end_date - from_date).days
    pbar = tqdm(total=days)
    filename = 'analytics_{}.csv'
    url = API_MANAGEMENT_URL + '/management/api/analytics/{}/analytics_{}.csv'
    headers = {
        'Cookie': cookie
    }
    invalid_days = []

    for day in (from_date + timedelta(i) for i in range(days)):
        filepath = os.path.join(output_dir, filename.format(day))
        resp = requests.get(url.format(api, day), headers=headers)

        if resp.status_code not in [200, 501]:
            resp.raise_for_status()
        elif resp.status_code == 501:
            invalid_days.append(day)
        else:
            with open(filepath, 'w') as f:
                f.write(resp.text)

        pbar.update(1)

    pbar.close()

    if invalid_days:
        print('Días no descargados:')
        for day in invalid_days:
            print(day)


if __name__ == '__main__':
    download()
