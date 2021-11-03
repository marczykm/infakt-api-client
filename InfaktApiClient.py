import argparse
import yaml
import coloredlogs
import json
import logging
import os
import datetime
import shelve
import requests
import time

from Invoice import Invoice

coloredlogs.install(level="INFO")
log = logging.getLogger("InfaktApiClient")


class InfaktApiClient:
    INFAKT_API_URL = 'https://api.infakt.pl:443/api/v3/'

    def __init__(self, configuration_file="infakt-api-client.yaml"):
        self.log = logging.getLogger("InfaktApiClient")
        self.log.info("InfaktApiClient logger initialized")
        self._loadConfiguration(configuration_file)

    def _loadConfiguration(self, configuration_file):
        try:
            config_data = open(
                os.path.expanduser(
                    configuration_file
                ),
                'r'
            ).read()
        except IOError:
            raise Exception('Cannot open configuration file ({file})!'.format(file=configuration_file))
        try:
            self.config = yaml.load(config_data, Loader=yaml.FullLoader)
        except Exception as yaml_error:
            raise Exception('Configuration problem: {error}'.format(error=yaml_error))

    def findInvoice(self, invoiceNum):
        headers = {'X-inFakt-ApiKey': self.config['infakt']['x-api-key']}
        response = requests.get(self.INFAKT_API_URL + "invoices/" + str(invoiceNum) + ".json", headers=headers)
        invoice = Invoice(response.json())
        log.info(invoice)
        return invoice
