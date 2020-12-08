import requests, base64, json
from BannedSellers import BannedSellers


def get_token():
	app_settings = {
		'client_id': 'GraciaGu-Scraper-PRD-cf788fdd4-893b9b52',
		'client_secret': 'PRD-f788fdd4768d-dc56-41ae-8dab-7c96',
		'ruName': 'Gracia_Gu-GraciaGu-Scrape-vawoghhy'}

	auth_header_data = app_settings['client_id'] + ':' + app_settings['client_secret']
	encoded_auth_header = base64.b64encode(str.encode(auth_header_data))
	encoded_auth_header = str(encoded_auth_header)[2:len(str(encoded_auth_header)) - 1]

	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": "Basic " + str(encoded_auth_header)
	}

	body = {
		"grant_type": "client_credentials",
		"redirect_uri": app_settings['ruName'],
		"scope": "https://api.ebay.com/oauth/api_scope"
	}

	token_url = "https://api.ebay.com/identity/v1/oauth2/token"

	response = requests.post(token_url, headers=headers, data=body)
	response_json = response.json()
	try:
		access_token = response_json['access_token']
	except:
		print(response_json['error_description'])  # if errors

	return access_token


def api_request(book_id, max_price, access_token):
	base_url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?'
	banned_sellers = '|'.join(BannedSellers)
	filter_url = 'q='+book_id+'&filter=price:[..'+max_price+'],priceCurrency:USD,excludeSellers:{'+banned_sellers+'}'
	complete_url = base_url+filter_url

	headers = {
		'Authorization': 'Bearer '+access_token
	}

	response = requests.get(url=complete_url, headers=headers)

	print(response.json())
	# pretty print
	# print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
	import time
	s = time.time()
	book_id = '0385265042'
	max_price = '200'
	api_request(book_id, max_price, get_token())
	print(time.time()-s > 7200)



