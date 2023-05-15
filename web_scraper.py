import requests
from bs4 import BeautifulSoup
import re
import csv

URL = "https://www.nordnet.dk/markedet/aktiekurser"
page = requests.get(URL, timeout=(3.05, 27))

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", {"class": "FlexTable__StyledDiv-sc-v6wpic-0"})
# Skip det første row fordi det en header¨
aktiepriser = results.contents[1:]


def cleanText(aktie):
    removePrefix = aktie.replace("KøbSælgDenmark", "")
    # Split tekst i en liste af ord
    words = removePrefix.split()

    # Fang de næste 5 ord for at få splittet firma navn, fra aktier værdier.
    for i in range(min(5, len(words))):
        # Split det første ord på + og - tegn
        words[i] = re.split(r'\+|-', words[i])

    words = [item for sublist in words for item in sublist]

    dictionary = {"name": ""}
    count = 0
    for word in words:
        if not any(i.isdigit() for i in word):
            dictionary["name"] = dictionary["name"] + word
        else:
            if len(dictionary["name"]) > 1:
                count += 1

                if count == 1:
                    dictionary["Idag Procent"] = word
                if count == 2:
                    dictionary["Idag Plus/Minus"] = word
                if count == 3:
                    dictionary["Seneste"] = word
                if count == 4:
                    dictionary["Køb"] = word
                if count == 5:
                    dictionary["Sælg"] = word
                    print(word)

    return dictionary


companies = []
for aktie in aktiepriser:
    aktieObj = cleanText(aktie.text)
    companies.append(aktieObj)


# Gem i database/csv fil

# name of csv file
filename = "aktiepriser.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=companies[0].keys())

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(companies)
