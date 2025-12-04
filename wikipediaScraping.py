import requests

url="https://www.wikipedia.com"
try:
    response=requests.get(url)
    response.raise_for_status()
    print(response.text)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occured:{http_err}")
except requests.exceptions.ConnectionError as conne_err:
    print(f"Connection error occured{conne_err}")
except requests.exceptions.Timeout as time_err:
    print(f"Timeout erro occured{time_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occured:{req_err}")