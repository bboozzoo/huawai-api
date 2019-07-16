#!/usr/bin/env python3

import argparse
import logging
import time

from huawei_api import HuaweiAPI


def parse_arguments():
    parser = argparse.ArgumentParser(description='monitor')
    parser.add_argument("--user",
                        help="Username to log in",
                        default="admin",
                        required=False)
    parser.add_argument("--password",
                        help="password to log in",
                        required=True)
    parser.add_argument("--debug",
                        help="enable debug log",
                        required=False,
                        action='store_true',
                        default=False)
    parser.add_argument("--ip",
                        help="Modem IP address",
                        default="192.168.8.1",
                        required=False)
    return parser.parse_args()


def main(args):
    api = HuaweiAPI(host=args.ip)
    api.ping()
    time.sleep(1)
    api.login(args.user, args.password)
    band = api.net_mode_list()
    logging.info('band: %s', band)
    while True:
        signal = api.device_signal()
        if signal["band"]:
            logging.info("RSRQ: %4s RSRP: %4s RSSI: %4s SINR: %4s LAC: %4s",
                         signal["rsrq"],
                         signal["rsrp"],
                         signal["rssi"],
                         signal["sinr"],
                         signal["cell_id"])
        time.sleep(1)


if __name__ == '__main__':
    args = parse_arguments()
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level,
                        format='%(asctime)-15s: %(message)s')
    try:
        main(args)
    except KeyboardInterrupt:
        pass
