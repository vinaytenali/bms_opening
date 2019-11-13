
import os
import requests

from argparse import ArgumentParser
from bs4 import BeautifulSoup

from mailsender import SendEmail

SUBJECT = "Movie tickets are open"
BODY = "BMS bookings for theater: {} is open for your movie on BookMyShow @ {}."

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

def search_venue(link, venue, to_address):
	if not to_address:
		to_address = EMAIL_ADDRESS
	source = requests.get(link).text
	soup = BeautifulSoup(source, 'lxml')
	for m in soup.find_all('meta'):
		try:
			if m['property'] == 'al:android:url':
				if m['content'].rsplit("/", 1)[1] != link.rsplit("/", 1)[1]:
					return
				else:
					break
		except:
			pass

	for bms_venue in soup.find_all('a', class_="__venue-name"):
		if venue.strip().lower() in bms_venue.text.strip().lower():
			se = SendEmail(subject=SUBJECT,
						   body=BODY.format(venue, link),
						   from_address=EMAIL_ADDRESS,
						   password=EMAIL_PASSWORD,
						   to_address=to_address)
			se.send_email()
			print("Email sent successfully to {}".format(to_address))


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("-l", "--bms_link", required=True,
						help="Enter the bookmyshow movie booking page link")
	parser.add_argument("-v", "--venue", required=True,
						help="Enter the theater name")
	parser.add_argument("-t", "--to", nargs='*', help="Enter the theater name")
	args = parser.parse_args()
	search_venue(args.bms_link, args.venue, args.to)

# python scrape.py -v "AMB Cinemas" -l "https://in.bookmyshow.com/buytickets/doctor-sleep-hyderabad/movie-hyd-ET00104940-MT/20191114"