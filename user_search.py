#!/usr/bin/env python3
import requests
import json
import warnings
import os
import logging

warnings.filterwarnings("ignore")

#Wing Controller info
wlc = "<IP ADDRESS OR DNS NAME>"
login = {"user":"<NAME>","password":"<PASSWORD>"}

# rf-domain name or device name
rf_domain = '<RF-DOMAIN>'
#user to search
username ='<USER NAME>'


baseurl = 'https://{}/rest'.format(wlc)

HEADERS= {
    'Content-Type': 'application/json'
    }

#-------------------------
# logging file and info
PATH = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
	filename='{}/user_search.log'.format(PATH),
	filemode='a',
	level=os.environ.get("LOGLEVEL", "INFO"),
    format= '%(asctime)s: %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)


def get_api_token():
    url = '{}/v1/act/login'.format(baseurl)
    try:
        r = requests.get(url, headers=HEADERS, verify=False, auth=(login['user'], login['password']), timeout=3)
    except:
        raise TypeError("API request failed")
    data = json.loads(r.text)
    auth_token = data['data']['auth_token']
    return(auth_token)

def close_api_session():
    url = '{}/v1/act/logout'.format(baseurl)
    try:
        r = requests.post(url, headers=HEADERS, verify=False, timeout=3)
    except:
        raise TypeError("API request failed")
    try:
        data = json.loads(r.text)
    except:
        logmsg = r.text
        log_msg = "Closing sessions {} failed with message: {}".format(HEADERS['cookie'],logmsg)
        logging.error(log_msg)
        raise TypeError("Failed to close session")
    if 'return_code' in data:
        if data['return_code'] != 0:
            logging.error("\n\nClosing session returned error {} for sessions {}").format(data['return_code'],HEADERS['cookie'])
        #else:
        #    print("\n\nSuccessfully closed session")

def post_api_call(url, rf_domain=None, device=None):
    url = '{}{}'.format(baseurl,url) 
    if rf_domain:
        payload = "{\n\t\"rf-domain\":\"RF_DOMAIN\"\n}"
        payload=payload.replace('RF_DOMAIN',rf_domain)
    elif device:
        payload = "{\n\t\"device\":\"DEVICE\"\n}"
        payload=payload.replace('DEVICE',device)
    else:
        payload = {}
    try:
        r = requests.post(url, headers=HEADERS, data=payload, verify=False, timeout=3)
    except:
        log_msg = "API request {} failed for site {}".format(url, rf_domain)
        logging.error(log_msg)
        raise TypeError(log_msg)
    try:
        data = json.loads(r.text)
    except:
        logmsg = r.text
        log_msg = "API post call failed with message: {}".format(HEADERS['cookie'],logmsg)
        logging.error(log_msg)
        raise TypeError("Failed to read info from API request {} for site {}")
    if data['return_code'] == 0:
        return(data['data'])
    else:
        log_msg = "{} returned code {}\n{}".format(url,data['return_code'],data['errors'])
        logging.error(log_msg)
        raise TypeError("{}".format(data['errors']))



def clientSearch(rf_domain,username):
    user = {}
    global HEADERS
    auth_token = get_api_token()
    HEADERS['cookie']='auth_token={}'.format(auth_token)
    url = '/v1/stats/wireless/client'
    try:
        data = post_api_call(url,rf_domain = rf_domain)
    except TypeError as e:
        raise TypeError(e)
    except:
        raise TypeError("Unknown Error")
    for client in data:
        if username in client['username']:
            user['apname'] = client['ap_hostname']
            user['apmac'] = client['ap']
            user['ipaddr'] = client['ip']
            user['mac'] = client['mac']
            user['wlan'] = client['wlan']
    return(user)



def main():
    data = {}
    global rf_domain
    global username

    #getRfDomainList()
    try:
        data = clientSearch(rf_domain, username)
    except TypeError as e:
        print(e)
        exit()
    except:
        print('Unknown')
        exit()
    print("{:^24}{:^24}{:^24}{:^24}{:^24}{:^24}".format('User','SSID','IP Address','MAC Address','Access Point','AP MAC'))
    print("{:^24}{:^24}{:^24}{:^24}{:^24}{:^24}".format(username,data['wlan'],data['ipaddr'],data['mac'],data['apname'],data['apmac']))

    close_api_session()

if __name__ == '__main__':
    main()