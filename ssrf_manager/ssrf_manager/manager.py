import click

from .config import load_config
from .actions import start_backend, start_frontend
from .processes import check_ports, show_processes
from .tui import launch_tui

@click.group()
@click.option("--backend-port", default=None, type=int)
@click.option("--frontend-port", default=None, type=int)
@click.option("--headless", is_flag=True, default=False)
@click.pass_context
def cli(ctx, backend_port, frontend_port, headless):
    ctx.obj = load_config(backend_port, frontend_port, headless)

@cli.command()
@click.pass_obj
def backend(cfg):
    start_backend(cfg)

@cli.command()
@click.pass_obj
def frontend(cfg):
    start_frontend(cfg)

@cli.command()
@click.pass_obj
def ports(cfg):
    check_ports(cfg.backend_port, cfg.frontend_port)

@cli.command()
@click.pass_obj
def processes(cfg):
    show_processes()

@cli.command()
@click.pass_obj
def tui(cfg):
    launch_tui(cfg)
