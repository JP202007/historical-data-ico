import requests
import re
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup

#NAME=['dragon-coins','bankera','envion','elastos','zeepin','neurotoken','swissborg','nexo','celsius','odyssey','leadcoin',
 #     'lendroid-support-token','arcblock','4new','hycon','gonetwork','fusion','shopin','hurify','datawallet','wepower',
  #    'nucleus-vision','mobius','0chain','fantom','fuzex','pundi-x','cardstack','constellation','bnktothefuture','jet8',
   #   'hydro-protocol','trade-token','proximax','shipchain','restart-energy-mwat','trakinvest','moneytoken','aergo','edge',
    #  'merculet','faceter','refereum','sentinel-protocol','rentberry','bezant','pchain','libra-credit','tokenomy','polyswarm',
     # 'essentia','storiqa','atonomi','apex','fintrux-network','liquidity-network','credits','origintrail','thekey','colu-local-network',
      #'selfkey','pecunio','fluz-fluz','holo','farmatrust','lala-world','babb','banca','theta','insureum','trinity-network-credit',
    #  'carvertical','bluzelle','te-food','amlt','hoqu','bobs-repair','gochain','open-platform','rightmesh','remme','rate3',
     # 'insights-network','skrumble-network','aidcoin','cryptaldash','oneledger','blockport','fortknoxster','coinfi','ink-protocol',
     # 'bee-token','ilcoin','block-array','winding-tree','latiumx','sentinel-chain','adbank','unibright','dacc','contentbox',
     # 'dether','matrix-ai-network','saifu','lympo','foam','matrix-ai-network','fundrequest','napoleonx','seele','metronome',
 #     'adhive','robotina','modultrade','loyalcoin','metadium','devery','decentralized-machine-learning','airbloc','lendingblock',
#      'pikciochain','lamden','phantasma','phantasma','experty','0xcert','nos','syncfab','switcheo','tomochain','seal-network',
  #    'ip-exchange','morpheus-network','omnitude','sharpe-platform-token','cargox','elysian','bitrewards','belugapay','aurora-dao',
  #    'morpheus-labs','lemochain','alttex','nebula-ai','coinvest','sether','simdaq','patron','brickblock','cova','rotharium',
   #   'blitzpredict','asura-coin','auctus','bgogo-token','eristica','ternio','odem','menlo-one','kleros','talao','signals-network',
    #  'fortuna','zilliqa','live-stars','hirematch','plancoin','sonder','crowdholding','blocklancer','crystal-token','crypto-improvement-fund',
  #    'tokia','well','bitether','galaxy-esolutions','energitoken','daneel','naviaddress','consentium','budbo','blockmesh',
   #   'traxia','sharder','cashbet-coin','transcodium','daostack','invictus-hyperion-fund','skychain']
#NAME=['eos','orbs','hedera-hashgraph','covalent','cryptosolartech','crypterium','videocoin','dcc','hybridblock','alchemy',
 #     'endor','yggdrash','origin-protocol','herocoin','metahash','tbis','shivom','solve','bloom','tradove','vault12','synthetix',
 #     'havven','electrifyasia','origo','sparkster','grapevine','origo','usechain','nervos-network','moonx','gbx','thrive',
  #    'flogmall','mxc','medicalchain','uservice','blue-whale','tutellus','heronode','dxchain','soar','cedex','silkchain',
   #   'edenchain','axpire','quarkchain','ultrain','dock','drep','caspian','ttc','lgo','dav','ankr','cgcx','agentmile','newton',
    #  'glitzkoin','mandala','vouchforme','mossland','rate3','debitum','sweetbridge','nauticus','foam','cybertrust','gameflip',
NAME=['multiversum','disciplina','pulsar','lambda','quadrantprotocol','blockcloud','squeezer','bitrent','gatcoin','alchemint',
      'bitguild','friendz','bitmax','effect-ai','carry','kairos','shift','zeex','traceto','cloudmoolah','globitex','adshares',
      'aitheon','kora-network-token','luna','codex','xyo','sapien','carry','themis','grain','coinmetro','eligma','oceanex',
      'copytrack','armpack','valid','connectjob','airbloc','districts','verime','skale','snapparazzi','pdx','lydian','current']


for name in NAME:
    url = 'https://coinmarketcap.com/currencies/' + name + '/historical-data/?start=20180101&end=20900401'
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
