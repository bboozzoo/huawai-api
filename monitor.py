#!/usr/bin/env python2

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
    api = HuaweiAPI(host=args.ip, user=args.user, passwd=args.password)
    while True:
        signal = api.device_signal()
        if signal["band"]:
            logging.info("Current Band: B" + signal["band"])
            logging.info("RSRQ: " + signal["rsrq"])
            logging.info("RSRP: " + signal["rsrp"])
            logging.info("RSSI: " + signal["rssi"])
            logging.info("SINR: " + signal["sinr"])
        time.sleep(1)


if __name__ == '__main__':
    args = parse_arguments()
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    main(args)
