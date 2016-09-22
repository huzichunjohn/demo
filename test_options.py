import click
import sys

@click.command()
@click.option('--pos', nargs=2, type=float)
def findme(pos):
    click.echo('%s / %s' % pos)


@click.command()
@click.option('--item', type=(unicode, int))
def putitem(item):
    click.echo('name=%s id=%d' % item)

@click.command()
@click.option('--message', '-m', multiple=True)
def commit(message):
    click.echo('\n'.join(message))

@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)

#@click.command()
#@click.option('--shout/--no-shout', default=False)
#def info(shout):
#    rv = sys.platform
#    if shout:
#        rv = rv.upper() + '!!!!111'
#    click.echo(rv)

#@click.command()
#@click.option('--shout', is_flag=True)
#def info(shout):
#    rv = sys.platform
#    if shout:
#        rv = rv.upper() + '!!!!111'
#    click.echo(rv)

@click.command()
@click.option('/debug;/no-debug')
def log(debug):
    click.echo('debug=%s' % debug)

@click.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info(transformation):
    click.echo(getattr(sys.platform, transformation)())

if __name__ == "__main__":
    info()
