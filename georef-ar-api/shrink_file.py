#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para retocar estilo de reportes html generados a partir de jupyter
notebooks.
"""
import os
import click

WHITE_LINE = """<div class="cell border-box-sizing code_cell rendered">


</div>"""

IMPORT_LOG = "importing Jupyter notebook from georef_log_analysis.ipynb"
IMPORT_ANA = "importing Jupyter notebook from georef_analytics_analysis.ipynb"


@click.command()
@click.option('--file', help='Nombre del archivo', required=True)
def remove_empty_lines(file):
    if os.path.isfile(file):
        with open(file, 'r+') as f:
            data = f.read().replace(WHITE_LINE, '').replace(
                IMPORT_LOG, '').replace(IMPORT_ANA, '')
            f.seek(0)
            f.write(data)
            f.truncate()
        # with open(file, 'w') as f:
            # f.write(data)
    else:
        raise 'No se encontró el archivo'


if __name__ == '__main__':
    remove_empty_lines()
