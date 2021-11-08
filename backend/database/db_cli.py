import click
import MySQLdb
from flask import Flask, current_app
from flask.cli import with_appcontext

from backend.utility.db_wrapper import get_cursor


def makeDb(cursor):
    with current_app.open_resource('database/schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))


def addData(cursor):
    with current_app.open_resource('database/testdata.sql') as f:
        cursor.execute(f.read().decode('utf8'))


def delete_db(cursor):
    cursor.execute("drop database rica;")
    cursor.execute("CREATE DATABASE rica;")


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
