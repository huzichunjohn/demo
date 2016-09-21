import click

CONTEXT_SETTINGS = dict(
    default_map={'runserver': {'port': 5000}}
)

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

if __name__ == "__main__":
    cli()
