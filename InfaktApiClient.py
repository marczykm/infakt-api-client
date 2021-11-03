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

    def _prepareHeaders(self):
        headers = {'X-inFakt-ApiKey': self.config['infakt']['x-api-key']}
        return headers

    def findInvoice(self, invoiceNum):
        response = requests.get(self.INFAKT_API_URL + "invoices/" + str(invoiceNum) + ".json", headers=self._prepareHeaders())
        invoice = Invoice(response.json())
        log.info(invoice)
        return invoice

    def generatePdf(self, invoiceNum):
        response = requests.get(self.INFAKT_API_URL + "/invoices/" + str(invoiceNum) + "/pdf.json?document_type=original&locale=pe", headers=self._prepareHeaders())
        fileName = str(invoiceNum)+".pdf"
        with open(fileName, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
            fd.close()
        log.info("Saved invoice as {}".format(fileName))
    
    def sendViaEmail(self, invoiceNum, email, sendCopy=True):
        data = { "print_type":"original", "locale":"pe", "recipient":email, "send_copy": sendCopy }
        response = requests.post(self.INFAKT_API_URL + "invoices/" + str(invoiceNum) + "/deliver_via_email.json", headers=self._prepareHeaders(), data=data)
        
        log.info(response.status_code)
    
    def createInvoice(self, clientId, saleDate, invoiceDate, paymentDate, grossPrice):
        payload = {
            "invoice": {
                "client_id": str(clientId),
                "payment_method": "transfer",
                "sale_date": saleDate,
                "invoice_date": invoiceDate,
                "payment_date": paymentDate,
                "services": [
                    {
                        "name": "Wytwarzanie oprogramowania",
                        "gross_price": str(int(grossPrice*100)),
                        "tax_symbol": 23
                    }
                ]
            }
        }
        response = requests.post(self.INFAKT_API_URL + "invoices.json", headers=self._prepareHeaders(), json=payload)
        log.info(response.status_code)
        log.info(response.content)
        invoice = Invoice(response.json())
        log.info(invoice)
        return invoice
    
    def deleteInvoice(self, invoiceNum):
        response = requests.delete(self.INFAKT_API_URL + "invoices/" + str(invoiceNum) + ".json", headers=self._prepareHeaders())
        log.info(response.status_code)

        