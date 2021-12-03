from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import Invoice
import InfaktApiClient
import calendar
import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("Niedasieukryc*8")
}

@auth.verify_password
def verify_password(username, password):
	if username in users and \
		check_password_hash(users.get(username), password):
		return username


def generateAndSend(gross_price):
	client_id = 9220335
	today = datetime.date.today()
	first = today.replace(day=1)
	previousMonth = (first - datetime.timedelta(days=1)).month
	previousYear = (first - datetime.timedelta(days=1)).year
	r = calendar.monthrange(previousYear, previousMonth)
	lastDayOfPreviousMonth = r[1]
	sale_date = str(previousYear) + "-" + str(previousMonth) + "-" + str(lastDayOfPreviousMonth)
	invoice_date = sale_date
	today = datetime.date.today()
	payment_date = str(today.year) + "-" + str(today.month) + '-10'
	gross_price = float(gross_price)
	email = 'marcin.marczyk@dataart.com'
	client = InfaktApiClient.InfaktApiClient()
	invoice = client.createInvoice(client_id, sale_date, invoice_date, payment_date, gross_price)
	# client.findInvoice(invoice.id)
	client.sendViaEmail(invoice.id, email)
	# client.generatePdf(invoice.id)
	# client.deleteInvoice(invoice.id)
	return invoice

@app.route("/", methods=('GET', 'POST'))
@auth.login_required
def index():
	app.logger.info("auth: " + str(auth.current_user()))
	if request.method == 'POST':
		gross_price = request.form['gross_price']
		invoice = generateAndSend(gross_price)
		return render_template('index.html', invoice_number=invoice.number)
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
