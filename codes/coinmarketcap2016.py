import requests
import re
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup

NAME=['waves','iconomi','golem','singulardtv','lisk','firstblood','digixdao','synereo','decent','neo','lykke','komodo',
      'kibo-lotto','vslice','ico-openledger','etcwin','incent','pluton','ark','blockpay','hacker-gold','stratis','golos',
      'blockcdn','mass-coin','eboost','nexium','egaas','decentralized-capital']

for name in NAME:
    url = 'https://coinmarketcap.com/currencies/' + name + '/historical-data/?start=20160101&end=20170401'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X10_15_4) AppleWebKit '
                      '/ 537.36(KHTML, like Gecko) Chrome / 81.0.4044.138 Safari / 537.36',
        'X-Requested-With': 'XMLHttpRequest'}

    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    print(url)
    p_soup = soup(response.text, "html.parser")

    if p_soup.find('div', {'class': 'owj4iq-0 qQkOx'}):
        print('Sorry, we could not find your page')
    elif p_soup.find('div', {'class': 'cmc-table cmc-table--empty sc-1yv6u5n-0 jONMPu'}):
        print('no data to display')
    elif p_soup.find('div', {'class': 'cmc-tab-charts o318p2-0 AyKde'}):
        print('token not exist')
    elif len(p_soup.find('div', {'class': 'cmc-details-panel-price jta9t4-0 fcilTk'}))==2:
        print('This project is featured as an Untracked Listing')
    else:
        html = response.text
        reg1 = re.compile(r'"quotes"([\s\S]*?),"related":')
        data = reg1.findall(html)
        data = data[0]
        reg2 = re.compile(r'"time_open":"([\s\S]*?)T00:00:00.000Z')
        day = reg2.findall(data)
        reg3 = re.compile(r'"close":([\s\S]*?),"volume"')
        close = reg3.findall(data)
        close = np.array(close, dtype='float32')
        reg4 = re.compile(r'"volume":([\s\S]*?),"market_cap"')
        volume = reg4.findall(data)

        day = day[0:]
        close = close[0:]
        volume = volume[0:]

        df = pd.DataFrame({"day": day, "asset": name, "close": close, "volume": volume})
        # df_all=df_all.append(df)
        print(name)
        df.to_csv(name + ".csv", header=True, index=False)
    time.sleep(10)
# df_all.to_csv(".cvs",header=True,index=False)
