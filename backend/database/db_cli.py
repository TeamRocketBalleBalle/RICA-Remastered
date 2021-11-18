import os

import click
import MySQLdb
from dotenv import load_dotenv
from flask import current_app
from flask.cli import with_appcontext

load_dotenv()

dbName = os.getenv("RICA_MYSQL_DB", 'rica')


def makeDb(cursor):
    cursor.execute(f"USE {dbName};")
    with current_app.open_resource('database/schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))


def addData(cursor):
    query = f"use {dbName};"
    cursor.execute(query)
    with current_app.open_resource('database/testdata.sql') as f:
        cursor.execute(f.read().decode('utf8'))


def delete_db(cursor):
    query = f"DROP DATABASE {dbName};"
    cursor.execute(query)
    query = f"CREATE DATABASE IF NOT EXISTS {dbName};"
    cursor.execute(query)


@click.command('create-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    conn = current_app.mysql.connection
    cursor = conn.cursor()
    makeDb(cursor)
    click.echo('Initialized the database.')
    cursor.close()
    conn.commit()


@click.command('fill-testdata')
@with_appcontext
def testdata_db_command():
    conn = current_app.mysql.connection
    cursor = conn.cursor()
    addData(cursor)
    try:
        cursor.close()
    except MySQLdb.IntegrityError:
        click.echo("Data already present in database")
    else:
        click.echo('Data inserted in database')
    finally:
        conn.commit()


@click.command('delete-db')
@with_appcontext
def delete_db_command():
    conn = current_app.mysql.connection
    cursor = conn.cursor()
    delete_db(cursor)
    cursor.close()
    conn.commit()
    click.echo("Database deleted")
