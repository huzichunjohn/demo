import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--force', default=True, help="Dropped the database anyway.")
@click.argument('name')
def dropdb(force, name):
    click.echo(force)
    click.echo('Dropped the database: %s.' % name)

if __name__ == "__main__":
    cli()
