import argparse
import json
import pathlib
import os
from requests_oauthlib import OAuth1Session
from sys import exit
import webbrowser

def get_request_token(url, id, secret):
    request_token_url = f'{url}/oauth1/request'
    oauth = OAuth1Session(id, client_secret=secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    return (oauth, fetch_response.get('oauth_token'), fetch_response.get('oauth_token_secret'))

def get_access_token(url, id, secret, owner_key, owner_secret, verifier):
    oauth = OAuth1Session(id, client_secret=secret, resource_owner_key=owner_key, resource_owner_secret=owner_secret, verifier=verifier)
    access_token_url = f'{url}/oauth1/access'
    oauth.fetch_access_token(access_token_url)
    return oauth

def get_post_to_publish():
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('--post_path', type=pathlib.Path, required=True)
    args = vars(parser.parse_args())
    post_filename = args['post_path'].stem
    post_publication_date, post_title = post_filename.split(" - ")
    return {
        'title': post_title,
        'content': args['post_path'].read_text(),
        'status': 'future',
        'date': f'{post_publication_date} 08:00:00',
        'categories': [769254464]
    }

def main():
    # Parse the arguments
    full_path = os.path.realpath(__file__)
    with open(os.path.dirname(full_path) + "/wordpress.json", 'r') as json_file:
        wordpress_info = json.load(json_file)
        site_url = wordpress_info["site_url"]
        client_id = wordpress_info["client_id"]
        client_secret = wordpress_info["client_secret"]

    # Get a request token
    oauth, resource_owner_key ,resource_owner_secret = get_request_token(site_url, client_id, client_secret)

    # Redirect the user to the authorization URL
    base_authorization_url = f'{site_url}/oauth1/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    print('Validate the authorization of the app: a new tab will open in your favorite browser connecting to the url ' + authorization_url)
    webbrowser.open(authorization_url)

    # The user will be redirected to a callback URL with a verifier in the query string
    verifier = input('Please input the oauth_verifier: ')

    # Get an access token
    oauth = get_access_token(site_url, client_id, client_secret, resource_owner_key, resource_owner_secret, verifier)

    # You can now use oauth to make requests to the API
    url = f'{site_url}/wp-json/wp/v2/posts'
    data = get_post_to_publish()
    print(data)
    response = oauth.post(url, json=data)
    print(response)

if __name__ == '__main__':
    exit(main())