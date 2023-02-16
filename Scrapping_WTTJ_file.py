import requests
from bs4 import BeautifulSoup
import os
from pyairtable import Table, Api
import pandas as pd
import datetime
from GPT_functions import gpt_format

token = ''
base = ''

customers = ["homagames","datascientest","armis","mirakl","disneyland-paris","le-wagon"]

for company in customers:

    # URL of the website to be scraped
    url = "https://www.welcometothejungle.com/fr/companies/" + company + "/jobs"

    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the relevant data from the page using BeautifulSoup
    data = []
    for item in soup.find_all("header", class_="sc-1peil1v-2 KXluf"):
        title = item.find("span",class_="ais-Highlight-nonHighlighted").text
        contract = item.find("span",class_="sc-16yjgsd-3 cToOtz").text
        location = item.find("span", class_ = "sc-68sumg-0 gtzPXt").text
        for i in item.findAll('time'):
            if i.has_attr('datetime'):
                post_date = i['datetime'][:10]
        for i in item.findAll('a', href=True):
            job_link = "https://www.welcometothejungle.com" + i["href"]

            # Make a request to each open position of the company

            response = requests.get(job_link)
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            company_description = soup.find(id="about-section").text.replace("Who are they?","").replace("Qui sont-ils ?","")
            job_description = soup.find(id="description-section").text.replace("Job description", "").replace("Descriptif du poste","")
            # job_description = gpt_format(job_description)

            salary = "ND"
            education = "ND"
            experience = "ND"
            for i in soup.find_all("span", class_="sc-16yjgsd-3 bCCdzk"):
                if i.text[:7] == "Salaire":
                    salary = i.text[8:]
                elif i.text[:9] == "Éducation":
                    education = i.text[11:]
                elif i.text[:10] == "Expérience":
                    experience = i.text[12:]

            #TODO AJOUTER SALAIRE + EXPERIENCE + EDUCATION

            data.append({"Title": title, "Contract": contract, "Location": location, "Date": post_date, "Link": job_link,
                         "Company_description": company_description, "Job_description": job_description,
                         "Salary": salary, "Experience":experience, "Education": education})



    # data_DATAFRAME = pd.DataFrame(data)
    # data_dict = dict(data)

    # Connect to the Airtable database
    #table = Table('auth_token', 'base_id', 'table_name')
    table = Table(token, base, company)
    api = Api(token)
    # Store the data in the Airtable database
    for item in data:
        table.create(item)
    #
    # #TODO
    # # TODO AJOUTER CETTE COMMANDE POUR SCHEDULE VIA CRON FILE UN JOB REPETER TOUTE LES SEMAINES