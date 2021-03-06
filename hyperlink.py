import re
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Opening the file and reading it
with open("dummy.csv") as csvfile:
    csv_string = csvfile.read()
    # Sample URL tests
    # csv_string += "https://aws.amazon.com/premiumsupport/knowledge-center/athena-hive-cursor-error/"
    # csv_string += "\n https://aws.github.io/aws-eks-best-practices/"
    
# Where we'll store the URLs    
csv_set = set()

html_docs = []
titles = []


# Main function to extract all URL's that contain the keyword "aws"
def find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex, string)
    for url in urls:
        # if url[0].startswith("https://aws.amazon.com/premiumsupport/knowledge-center/"):
        if "aws" in url[0]:
            csv_set.add(url[0])

# Grabbing all non-empty strings
def get_nonempty(list_of_strings):
    for s in list_of_strings:
        if s:
            return s
             

# Invocation of main func       
find(csv_string)


# Getting the HTML docs for each URL
for url in csv_set:
    r = requests.get(url)
    html_docs.append(r.text)


# Web Parsing each url
for doc in html_docs:
    soup = BeautifulSoup(doc, "html.parser")
    list_of_strings = soup.get_text().splitlines()
    # Grabbing the title
    lst = get_nonempty(list_of_strings)
    # If the title of the webpage has quotes...
    if '"' in lst:
        # Replace it with an empty string 
        lst = lst.replace('"', '')
        
    titles.append(lst)

# Uncomment to see list of titles    
# print(titles)

# Turning the set back into a list
urls = list(csv_set)

# Matching the urls to titles
title_urls = list(zip(urls, titles))

# Uncomment to view list mapping titles to URL's
# print(title_urls)

# Writing our data to a new csv file
with open("out_csv.csv", "w", newline="") as new_csvfile:
    fieldnames = ["Hyperlinks"]
    writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in title_urls:
        writer.writerow({"Hyperlinks": '=HYPERLINK("' + item[0] +'","' + item[1]+'")' })

# Converting it to an xlsx without duplicates
# df = pd.read_csv("out_csv.csv", sep=",");
# df.drop_duplicates(subset=None, inplace=True)
# df.to_excel("final_output.xlsx", index=False)
