"""Herramienta para descargar CSVs con datos de consultas de API Management.
"""

import click
import pandas as pd
from tqdm import tqdm


API_MANAGEMENT_URL = 'https://apis.datos.gob.ar'
DATE_FMT = '%Y-%m-%d'


@click.command()
def log_cleaner():
    log_csv_path = './data/api-georef.csv'
    log_csv_path_clean = './data/api-georef-clean.csv'

    # log = open('../data/api-series.log')
    # log_csv = open(log_csv_path,mode='w')

    n_lines = 0

    with open('./data/api-georef.log') as log:
        with open(log_csv_path, mode='w') as log_csv:
            for line in log:
                line = log.readline()
                log_csv.write(line.replace(' ', ','))
                n_lines += 1

    log_headers = ['remote_addr',
                   '-',
                   'remote_user',
                   'time_local',
                   'request',
                   'status',
                   'body_bytes_sent',
                   'http_referer',
                   'http_user_agent']
    #                 'gzip_ratio']

    chunk_size = 5000
    pbar = tqdm(total=int(n_lines / chunk_size))

    reader = pd.read_csv(log_csv_path, chunksize=chunk_size, header=None)

    dfs = []

    for df_ in reader:
        df = df_.dropna().copy()

        df.iloc[:, 3] = df.iloc[:, 3] + ' ' + df.iloc[:, 4]
        df.drop(labels=4, axis=1, inplace=True)

        df.columns = log_headers

        df.loc[:, 'time_local'] = df['time_local'].apply(
            lambda x: x[1:-1].replace(' ', '')).copy()

        dt_time_local = pd.to_datetime(
            df['time_local'], format='%d/%b/%Y:%H:%M:%S-0300')
        dt_index = pd.DatetimeIndex(dt_time_local.apply(pd.Timestamp))
        dt_index_tz = dt_index.tz_localize('America/Argentina/Buenos_Aires')

        df.loc[:, 'time_local'] = dt_index_tz

        request = df.loc[:, 'request'].str.split(',').copy()

        df.loc[:, 'method'] = request.apply(lambda x: x[0]).copy()
        df.loc[:, 'uri'] = request.apply(lambda x: x[1].split('?')[0]).copy()
        df.loc[:, 'querystring'] = request.apply(
            lambda x: x[1].split('?')[-1]).copy()

        del request

        dfs.append(df)

        pbar.update(1)
    pbar.close()

    pd.concat(dfs).to_csv(log_csv_path_clean)

    print('\nLog file has been cleaned successfully.')
    return


if __name__ == '__main__':
    log_cleaner()
