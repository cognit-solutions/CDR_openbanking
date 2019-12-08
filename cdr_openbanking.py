import requests
import json
import logging
#import mongoquery




class OpenBanking:

    def __init__(self,bank=None,headers=None,proxies=None):

        self.banks = json.loads(open('participant.json','r').read())
        self.bank = {}
        for b in self.banks['data']:
            items = {"code":b['code'],"baseUrl":b['baseUrl'],
                    'supportedAPIs':b['supportedAPIs'],'brands':b['brands'],
                    'name':b['name']}

            #setup bank codes
            self.bank[b['code']] = items
            setattr(self,b['code'],items)
            setattr(self,b['code'].lower(),items)

        # setup headers 
        if headers == None:
            self.headers = {'Accept':'application/json','x-v': '1','x-min': '1'} 
        else:
            self.headers = headers

        self.proxies = proxies
        self.bank_code = bank

            

    # bank is one of the supported banks .. in Upper Case eg ANZ. 
    # params is a DICT of parameters for the API. eg params={'page':2, 'updated-since':'2019-06-01T00:00:00Z'}
    def getProducts(self,bank=None,params='',mquery=None):

        if bank:
            uri = self.bank[bank]['baseUrl']+'/banking/products'
            result_set = requests.get(uri,params=params,proxies=self.proxies,headers=self.headers)
        else:
            result_set = None
         
        return result_set
 

    def getProductDetail(self,bank,productId):
        uri = self.bank[bank]['baseUrl']+'/banking/products/' + productId
        result_set = requests.get(uri,proxies=self.proxies,headers=self.headers)
        return result_set