import requests

def saveFileasHTML(url: str, path: str):
    response = requests.get(url)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(response.text)

url = "https://ncdrc.nic.in/"
saveFileasHTML(url, "data/ncdrc.html")
