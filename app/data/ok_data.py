#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
import pandas as pd

def ok_data():
    """

    This functions returns the actual pump price from the OK gas station.

    There is the possibility for having Benzin 95 and diesel, to two
    dominant gas types. Others are thought to be useless


    Input:
        prod_number: int
            The OK defined prod number of those products
            536 = Benzin 95
            231 = Diesel DEFAULT VALUE
        start: datetime
            todays date DEFAULT VALUE
            THIS CAN ONLU HAVE FORMAT %Y-%M-%dT%H the rest is taken care of here
        end: datetime
            30 days back DEFAULT VALUE
            THIS CAN ONLU HAVE FORMAT %Y-%M-%dT%H the rest is taken care of here
        BOTH datetime objects will look something like -> 2022-12-30T23:00:00.000Z

    Raise:
        pandas Empty dataframe

    Output
        results: pd.Dataframe
                The end result of the api call the the ok site
    """
    start = datetime.now().strftime('%Y-%M-%dT%H')
    end = (datetime.now() - timedelta(days = 7)).strftime('%Y-%M-%dT%H')
    products = {'benzin95': 536, 'diesel': 231}

    payload={}
    products = {'benzin95': 536, 'diesel': 231}

    url = f"https://www.ok.dk/privat/produkter/ok-kort/prisudvikling/download?moms=true&varenr={products['diesel']}&from=2021-12-31T23:00:00.000Z&to=2022-12-30T23:00:00.000Z&inklAfgifter=true&per1000liter=false&pumpepris=true&perKg=false"

    headers = {
        'authority': 'www.ok.dk',
        'sec-ch-ua': '',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'text/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.31 Safari/537.36',
        'sec-ch-ua-platform': '',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ok.dk/privat/produkter/ok-kort/prisudvikling',
        'accept-language': 'en-GB',
        'cookie': 'ASP.NET_SessionId=wwnbtosmnuaiozk5up0lnese; CookieInformationConsent=%7B%22website_uuid%22%3A%22d26b4a62-456c-43cb-b729-e3f3e09e5ba2%22%2C%22timestamp%22%3A%222022-09-29T19%3A13%3A29.262Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fwww.ok.dk%2Fprivat%2Fprodukter%2Fok-kort%2Fbenzinpriser%22%2C%22consent_website%22%3A%22ok.dk%22%2C%22consent_domain%22%3A%22www.ok.dk%22%2C%22user_uid%22%3A%227915efae-b4e0-40cb-801b-a0dc19d599ea%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%5D%2C%22consents_denied%22%3A%5B%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F94.0.4606.31%20Safari%2F537.36%22%7D'
        }
    response = requests.request("GET", url, headers=headers, data=payload)

    col = []
    dates = []
    price = []

    for i, j in enumerate(response.text.split('\n')):
        temp = j.split(';')
        if i == 0:
            for k, n in enumerate(temp):
                if k == 0:
                    col.append(n[3:].replace('"', ''))
                else:
                    col.append(n.replace('"', '').strip())
        else:
            for k, n in enumerate(temp):
                if k == 0:
                    dates.append(temp[k].strip().replace('"', ''))
                else:
                    price.append(float(temp[k].replace('"', '').replace(',', '.').strip()))
    dates = dates[:-1]

    data = pd.DataFrame(columns = col)
    data[col[0]] = dates
    data[col[0]] = pd.to_datetime(data[col[0]], format = "%d-%m-%Y")
    data[col[1]] = price

    return data.sort_values(by = 'Dato', ascending = False)
