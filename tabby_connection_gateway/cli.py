import argparse
import asyncio
import logging
import os
import ssl

from .admin_server import AdminServer
from .gateway_server import GatewayServer


async def _main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--host', default='127.0.0.1', help='address to listen on')
    parser.add_argument('--port', default=9000, type=int, help='port to listen on')
    parser.add_argument(
        '--certificate', metavar='PATH', help='path to the SSL certificate. Enables SSL'
    )
    parser.add_argument('--private-key', metavar='PATH')
    parser.add_argument(
        '--ca',
        metavar='PATH',
        help='path to the CA certificate. Enables SSL client auth',
    )
    parser.add_argument(
        '--token-auth',
        action='store_true',
        help='enables token based auth using the token from the TABBY_AUTH_TOKEN env var',
    )
    parser.add_argument(
        '--admin-host',
        default='127.0.0.1',
        help='address to listen on for management requests',
    )
    parser.add_argument(
        '--admin-port',
        type=int,
        help='port to listen on for management requests',
    )
    parser.add_argument(
        '--admin-certificate',
        metavar='PATH',
        help='path to the SSL certificate for the management server',
    )
    parser.add_argument('--admin-private-key', metavar='PATH')
    parser.add_argument(
        '--admin-ca',
        metavar='PATH',
        help='path to the CA certificate for the management server',
    )
    args = parser.parse_args()

    if args.certificate and not args.private_key:
        parser.error('--private-key is required if --certificate is set')

    if args.token_auth and not os.getenv('TABBY_AUTH_TOKEN'):
        parser.error('TABBY_AUTH_TOKEN must be provided when using --token-auth')

    if args.admin_port:
        if (
            not args.admin_ca or
            not args.admin_certificate or
            not args.admin_private_key
        ):
            parser.error(
                '--admin-ca, --admin-certificate and --admin-private-key are all required when --admin-port is set'
            )

    logging.basicConfig(level=logging.INFO)

    ssl_context = None
    if args.certificate:
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH,
            cafile=os.path.realpath(args.ca) if args.ca else None,
        )
        ssl_context.load_cert_chain(
            os.path.realpath(args.certificate),
            os.path.realpath(args.private_key),
        )
        if args.ca:
            ssl_context.verify_mode = ssl.CERT_REQUIRED

    admin_ssl_context = None
    if args.admin_ca:
        admin_ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH,
            cafile=os.path.realpath(args.admin_ca),
        )
        admin_ssl_context.load_cert_chain(
            os.path.realpath(args.admin_certificate),
            os.path.realpath(args.admin_private_key),
        )
        admin_ssl_context.verify_mode = ssl.CERT_REQUIRED

    await GatewayServer(
        host=args.host,
        port=args.port,
        ssl=ssl_context,
        auth_token=os.getenv('TABBY_AUTH_TOKEN'),
    ).start()

    if args.admin_port:
        await AdminServer(
            host=args.admin_host,
            port=args.admin_port,
            ssl=admin_ssl_context,
        ).start()


def main():
    asyncio.get_event_loop().run_until_complete(_main())
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        os._exit(0)


if __name__ == '__main__':
    main()
