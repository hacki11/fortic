import logging
import sys

import click
from keepasshttp import keepasshttp
from fortic.fortinet import FortiClient
from fortic.keepassxc import KeePassXCClient

schema = "vpn://"


@click.group()
@click.option("--path", "-p", type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
              help="Directory or path to FortiSSLVPNclient.exe")
@click.help_option("-h", "--help")
@click.pass_context
def main(ctx, path):
    """
    Connect to Fortinet SSL VPN Gateway

    I need FortiSSLVPNclient.exe and will search in:

    \b
    - C:\\Program Files (x86)\\Fortinet\\SslvpnClient
    - C:\\Program Files\\Fortinet\\SslvpnClient
    - in -p/--path given to the command (as file or directory)
    - in FORTISSLVPN_HOME environment variable
    - availability in PATH variable
    """
    logging.basicConfig(format="[%(levelname)-5s] %(message)s", stream=sys.stdout, level=logging.DEBUG)
    ctx.obj = path
    pass


@click.command(help="Endpoint address")
@click.argument("url")
@click.option("-cd", "--credential-provider", type=click.Choice(['keepasshttp', 'keepassxc'], case_sensitive=False), default='keepassxc', show_default=True, help="Which credential provider shall be used")
@click.pass_context
def connect(ctx, url, credential_provider):
    try:
        client = FortiClient(ctx.obj)

        if credential_provider == 'keepasshttp':
            creds = get_credentials_keepass(url)
            client.connect(url, creds.login, creds.password)

        elif credential_provider == 'keepassxc':
            creds = get_credentials_keepassxc(url)
            client.connect(url, creds['login'], creds['password'])

        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


@click.command(help="Disconnect")
@click.pass_context
def disconnect(ctx):
    try:
        client = FortiClient(ctx.obj)
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


main.add_command(connect)
main.add_command(disconnect)


def get_credentials_keepass(url):
    search_url = schema + url
    logging.info("Retrieve KeePass credentials for '" + search_url + "'")
    credentials = keepasshttp.get(search_url)
    if credentials is None:
        raise Exception(
            "KeePass entry for '" + url + "' not found! Please add an entry with '" + search_url + "' as name or url")

    logging.info(f"Credentials found (User: {credentials.login})")
    return credentials


def get_credentials_keepassxc(url):
    search_url = schema + url
    logging.info("Retrieve KeePassXC credentials for '" + search_url + "'")
    keepassxc = KeePassXCClient()
    credentials = keepassxc.get_logins(search_url)
    logging.info(f"Credentials found (User: {credentials[0]['login']})")
    return credentials[0]


if __name__ == '__main__':
    main()
