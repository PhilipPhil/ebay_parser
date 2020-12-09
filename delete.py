import requests, base64, json
from BannedSellers import BannedSellers
from Token import Token


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


if __name__ == "__main__":
    Token = Token()
    book_id = '0385265042'
    max_price = '200'
    print(api_request(book_id, max_price, Token.get_token()))



