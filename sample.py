import requests

def saveFileasHTML(url: str, filename: str):
    response = requests.get(url)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

url = "https://cms.nic.in/"
saveFileasHTML(url, "data/ncdrc.html")
