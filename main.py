import InfaktApiClient
import coloredlogs
import logging
import argparse
import calendar
import datetime

parser = argparse.ArgumentParser(description='Infakt API Client')
parser.add_argument('--client_id',    required=False, dest='client_id',    help='client id')
parser.add_argument('--sale_date',    required=False,  dest='sale_date',    help='sale date')
parser.add_argument('--invoice_date', required=False, dest='invoice_date', help='invoice date')
parser.add_argument('--payment_date', required=False,  dest='payment_date', help='payment date')
parser.add_argument('--gross_price',  required=True,  dest='gross_price',  help='gross price')
parser.add_argument('--email',  required=False,  dest='email',  help='email')

args = vars(parser.parse_args())

client_id = args['client_id']
if (client_id == None):
	client_id = 9220335
sale_date = args['sale_date']
if (sale_date == None):
	today = datetime.date.today()
	first = today.replace(day=1)
	previousMonth = (first - datetime.timedelta(days=1)).month
	previousYear = (first - datetime.timedelta(days=1)).year
	r = calendar.monthrange(previousYear, previousMonth)
	lastDayOfPreviousMonth = r[1]
	sale_date = str(previousYear) + "-" + str(previousMonth) + "-" + str(lastDayOfPreviousMonth)
invoice_date = args['invoice_date']
if (invoice_date == None):
	invoice_date = sale_date
payment_date = args['payment_date']
if (payment_date == None):
	today = datetime.date.today()
	payment_date = str(today.year) + "-" + str(today.month) + '-10'
gross_price = float(args['gross_price'])
email = args['email']
if (email == None):
	email = 'marcin.marczyk@dataart.com'

coloredlogs.install(level="INFO")
log = logging.getLogger("main")
client = InfaktApiClient.InfaktApiClient()

log.info(client_id)
log.info(sale_date)
log.info(invoice_date)
log.info(payment_date)
log.info(gross_price)
log.info(email)

if __name__ == "__main__":
	log.info('Running main application')
	invoice = client.createInvoice(client_id, sale_date, invoice_date, payment_date, gross_price)
	client.findInvoice(invoice.id)
	client.sendViaEmail(invoice.id, email)
	client.generatePdf(invoice.id)
	# client.deleteInvoice(invoice.id)
	