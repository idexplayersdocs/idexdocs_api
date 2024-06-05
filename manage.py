#! /usr/bin/env python
"""Module to ensure an environment variable existes and has a value"""

# pylint: disable=c0116
import json
import os
import signal
import subprocess
import time
from typing import Dict

import click
import pyodbc


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


# Forced the variable APPLICATION_CONFIG to be production if not specified
setenv('APPLICATION_CONFIG', 'local')

APPLICATION_CONFIG_PATH = 'config'
DOCKER_PATH = 'docker'


def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f'{config}.json')


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f'{config}.yml')


def read_json_configuration(config: str) -> Dict:
    # Read configuration from the relative JSON file
    with open(app_config_file(config), encoding='utf-8') as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i['name'], i['value']) for i in config_data)

    return config_data


def configure_app(config):
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)


@click.group()
def cli():
    pass


def docker_compose_cmdline(commands_string=None):
    config = os.getenv('APPLICATION_CONFIG')
    configure_app(config)

    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f'The file {compose_file} does not exist')

    command_line = [
        'docker-compose',
        '-p',
        config,
        '-f',
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(' '))

    return command_line


def is_docker_running():
    try:
        subprocess.check_output(['docker', 'info'])
        return True
    except subprocess.CalledProcessError:
        click.echo(
            'Docker is not running. Please start docker before using this command'
        )
        return False


def run_sql(statements):
    connection_string = 'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={};UID={};PWD={};TrustServerCertificate=yes'.format(
        os.getenv('MSSQL_HOSTNAME'),
        os.getenv('MSSQL_USER'),
        os.getenv('MSSQL_SA_PASSWORD'),
    )

    conn = pyodbc.connect(connection_string)
    conn.autocommit = True

    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode('utf-8'):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('subcommand', nargs=-1, type=click.Path())
def compose(subcommand):
    if not is_docker_running():
        return

    configure_app(os.getenv('APPLICATION_CONFIG'))
    cmdline = docker_compose_cmdline() + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command
def init_mssql():
    configure_app(os.getenv('APPLICATION_CONFIG'))

    try:
        run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
    except pyodbc.DatabaseError:
        print(
            f"The database {os.getenv('APPLICATION_DB')} already exists and will not be created"
        )
    except Exception as e:
        print(e)


@cli.command
@click.option('--message', '-m', help='Migration message')
def makemigrations(message):
    """Run Alembic revision --autogenerate command."""
    configure_app(os.getenv('APPLICATION_CONFIG'))

    try:
        command = ['alembic', 'revision', '--autogenerate', '-m', message]
        subprocess.run(command)
    except Exception as e:
        print(e)


@cli.command
def migrate():
    """Run Alembic upgrade head."""
    configure_app(os.getenv('APPLICATION_CONFIG'))

    try:
        command = ['alembic', 'upgrade', 'head']
        subprocess.run(command)
    except Exception as e:
        print(e)


@cli.command
@click.option('--server', '-s', default='uvicorn', help='Application server')
def startapp(server):
    """Start FastAPI server"""
    configure_app(os.getenv('APPLICATION_CONFIG'))

    try:
        if server == 'uvicorn':
            command = ['uvicorn', 'asgi:app', '--reload']
        elif server == 'gunicorn':
            command = [
                'gunicorn',
                '-b',
                ':8000',
                '--reload',
                '-k',
                'uvicorn.workers.UvicornWorker',
                '--timeout',
                '500',
                'asgi:app',
            ]
        else:
            raise click.BadParameter('Server options are uvicorn or gunicorn.')
        subprocess.run(command)
    except Exception as e:
        print(e)


@cli.command()
@click.argument('args', nargs=-1)
def test(args):
    if not is_docker_running():
        return

    os.environ['APPLICATION_CONFIG'] = 'testing'
    configure_app(os.getenv('APPLICATION_CONFIG'))

    cmdline = docker_compose_cmdline('up -d')
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline('logs sqlserver-test')
    wait_for_logs(cmdline, 'Service Broker manager has started.')

    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = [
        'pytest',
        '-svv',
        '--cov=application',
        '--cov-report=term-missing',
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline('down')
    subprocess.call(cmdline)


if __name__ == '__main__':
    cli()
