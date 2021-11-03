import InfaktApiClient
import coloredlogs
import logging

coloredlogs.install(level="INFO")
log = logging.getLogger("main")
client = InfaktApiClient.InfaktApiClient()

if __name__ == "__main__":
	log.info('Running main application')
	client.findInvoice(41727411)