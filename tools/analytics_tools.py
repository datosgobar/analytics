
"""Herramienta para descargar CSVs con datos de consultas de API Management.
"""
import sys
import os
import requests
import click
from tqdm import tqdm
from datetime import datetime, date, timedelta
import zipfile
from glob import glob

import pandas as pd

from http.cookiejar import CookieJar
import mechanize

import json
import glob

API_MANAGEMENT_URL = 'https://apis.datos.gob.ar'
DATE_FMT = '%Y-%m-%d'

REPO_NAME = 'analytics'
REPO_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DIR_DATA_SDT = REPO_DIR + '/data/series-tiempo'
DIR_DATA_GR = REPO_DIR + '/data/georef'

PATHS = [DIR_DATA_SDT, DIR_DATA_GR]
APIS = ['series-tiempo-prod', 'georef-prod']

APIS_PATHS = {'series-tiempo-prod': DIR_DATA_SDT,
              'georef-prod': DIR_DATA_GR}

CREDENTIALS_FILE = '/config.json'
CREDENTIALS_PATH = REPO_DIR + CREDENTIALS_FILE


def printerr(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
    exit(1)


def get_first_last_file_date(directory):
    """Devuelve la fecha del archivo de analytics más reciente."""
    if not os.path.isdir(directory):
        os.makedirs(directory)
        return '2018-01-01'

    file_pattern = os.path.join(directory, "*.csv")
    dates_list = [file.split('/')[-1].split('.')[0][-10:]
                  for file in glob.glob(file_pattern)]

    return max(dates_list)


def get_cookie():
    json_credentials = CREDENTIALS_PATH
    login_site = 'https://apis.datos.gob.ar/management/ingresar/login'
    jsonfile = json.load(open(json_credentials))

    if login_site not in list(jsonfile.keys()):
        return 'wrong url'
    else:
        username = list(jsonfile[login_site][0].keys())[0]
        password = list(jsonfile[login_site][0].values())[0]

    br = mechanize.Browser()
    cj = CookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    br.open(login_site)
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()

    return cj


def download(api, cookie, output_dir, from_date, end_date, verbose=False):
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

    days = (end_date - from_date).days
    if verbose:
        print('Descargando archivos de {}...'.format(api))
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
        if verbose:
            pbar.update(1)

    if verbose:
        pbar.close()

        if invalid_days:
            print('Días no descargados:')
            for day in invalid_days:
                print(day)


def update_analytics(verbose=False):
    cookie = '; '.join(
        [cookie.name + '=' + cookie.value for cookie in get_cookie()])

    end_date = pd.datetime.today().strftime('%Y-%m-%d')

    for api, path in APIS_PATHS.items():
        from_date = get_first_last_file_date(path)
        if from_date is None:
            download(api=api, cookie=cookie,
                     output_dir=path, end_date=end_date, verbose=verbose)
        else:
            download(api=api, cookie=cookie, output_dir=path,
                     from_date=from_date, end_date=end_date, verbose=verbose)


if __name__ == '__main__':
    update_analytics(verbose=True)
