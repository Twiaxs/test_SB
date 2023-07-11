import requests

url = 'http://localhost:8000/api/deals/'
file_path = 'deals.csv'

with open(file_path, 'rb') as file:
    files = {'deals': file}
    response = requests.post(url, files=files)

print(response.text)
