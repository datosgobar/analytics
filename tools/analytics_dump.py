#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Métodos para generar un dump zipeado publicable de analytics."""

import os
import pandas as pd
import zipfile
from glob import glob
import os
import json


def process_series_analytics(df):
    """Remueve columnas para publicar analytics de series."""
    df_dropped = df.drop(columns=["id", "ip_address", "host", "request_time",
                                  "api_data", "token", "referer"],
                         errors="ignore")
    return df_dropped


def process_georef_analytics(df):
    """Remueve columnas e input de uris restingidas para publicar
    analytics de georef."""
    disclosive_uris = [
        "/georef/api/direcciones", "/georef/api/v1.0/direcciones",
        "/georef/api/ubicacion", "/georef/api/v1.0/ubicacion"
    ]

    df_dropped = df.drop(columns=["id", "ip_address", "host", "request_time",
                                  "api_data", "token", "referer"],
                         errors="ignore")

    df_dropped.loc[df_dropped.uri.isin(disclosive_uris), "querystring"] = None

    return df_dropped


def add_analytics_file_to_zip(zip_path, csv_path, process_function,
                              remove_after=False):
    """Agrega un CSV de analytics a un ZIP."""
    df_input = pd.read_csv(csv_path, encoding="utf8")
    df_output = process_function(df_input)

    with zipfile.ZipFile(zip_path, 'a', compression=zipfile.ZIP_DEFLATED) as zp:
        zp.writestr(os.path.basename(csv_path),
                    df_output.to_csv(encoding="utf8", index=False))

    if remove_after:
        os.remove(csv_path)


def create_analytics_zip(analytics_csv_pattern, analytics_zip,
                         process_function):
    # toma archivos de analytics ya comprimidos
    zipf = zipfile.ZipFile(analytics_zip)
    zipped_files = zipf.namelist()

    for csv_path in glob(analytics_csv_pattern):
        csv_filename = os.path.basename(csv_path)
        if csv_filename not in zipped_files:
            print("Adding {}...".format(csv_path))
            add_analytics_file_to_zip(
                analytics_zip, csv_path, process_function)


def main():
    REPO_NAME = "analytics"
    REPO_DIR = os.path.abspath(os.path.dirname(__file__))
    CREDENTIALS_FILE = '/config.json'
    CREDENTIALS_PATH = REPO_DIR + CREDENTIALS_FILE
    config = json.load(open(CREDENTIALS_PATH))

    create_analytics_zip(
        "data/series-tiempo/analytics_*.csv",
        config["analytics_series_zip"],
        process_series_analytics
    )

    create_analytics_zip(
        "data/georef/analytics_*.csv",
        config["analytics_georef_zip"],
        process_georef_analytics
    )


if __name__ == '__main__':
    main()
