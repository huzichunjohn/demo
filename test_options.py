import click
import os
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

@click.command()
@click.option('--name', prompt='Your name please')
def hello(name):
    click.echo('Hello %s!' % name)

@click.command()
@click.password_option()
#@click.option('--password', prompt=True, hide_input=True,
#              confirmation_prompt=True)
def encrypt(password):
    click.echo('Encrypting password to %s' % password.encode('rot13'))

#@click.command()
#@click.option('--username', prompt=True,
#              default=lambda: os.environ.get('USER', ''))
#def hello(username):
#    print('hello,', username)

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello():
    click.echo('hello world!')

#def abort_if_false(ctx, param, value):
#    if not value:
#        ctx.abort()
#
#@click.command()
#@click.option('--yes', is_flag=True, callback=abort_if_false,
#              expose_value=False,
#              prompt='Are you sure you want to drop the db?')
#def dropdb():
#    click.echo('Dropped all tables!')

@click.command()
@click.confirmation_option(help='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')


#@click.command()
#@click.option('--username')
#def greet(username):
#    click.echo('hello %s!' % username)

@click.command()
@click.option('--username', envvar='USERNAME')
def greet(username):
    click.echo('hello %s!' % username)

@click.command()
@click.option('paths', '--path', envvar='PATHS', multiple=True,
              type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)


def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@click.command()
@click.option('--rolls', callback=validate_rolls, default='1d6')
def roll(rolls):
    click.echo('Rolling a %d-sided dice %d time(s)' % rolls)

@click.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def copy(src, dst):
    for fn in src:
        click.echo('move %s to folder %s' % (fn, dst))

@click.command()
@click.argument('f', type=click.Path(exists=True))
def touch(f):
    click.echo(click.format_filename(f))

@click.command()
@click.argument('src', envvar='SRC', type=click.File('r'))
def echo(src):
    click.echo(src.read())

@click.command()
@click.argument('files', nargs=-1, type=click.Path())
def touch(files):
    for filename in files:
        click.echo(filename)

if __name__ == "__main__":
    touch()
