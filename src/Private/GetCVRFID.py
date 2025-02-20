from typing import Optional
import requests
from SetGlobalVariables import *

def getCVRFID(
        CVRFID: Optional[str] = None,
        timeout: float = 10.0,
        retries: int = 3,
        retry_delay: float = 1.0,
        )-> list :
    
    if retries < 0 :
        raise ValueError("Wert für retries darf nicht negativ sein: getCVRFID")
    
    url = f"{msrcApiUrl}/Updates?{msrcApiVersion}"

    _Headers = {'Accept': 'application/json'}
    
    _Proxies = {}
    if msrcProxy:
        _Proxies['http'] = msrcProxy
        _Proxies['https'] = msrcProxy

    _Auth = None
    if msrcProxyCredential:
        username, password = msrcProxyCredential.split(":")
        _Auth = requests.auth.HTTPProxyAuth(username, password)

    if MSRCAdalAccessToken:
        _Headers['Authorization'] = MSRCAdalAccessToken.create_authorization_header()
    
    try :
        if CVRFID is not None :
            Response = requests.get(url, headers=_Headers, auth=_Auth, proxies=_Proxies).json()['value']

            return [
                item['ID'] for item in Response if (item['ID'] == CVRFID and item['ID'] != '2017-May-B') 
            ]
        else :
            Response = requests.get(url, headers=_Headers, auth=_Auth, proxies=_Proxies).json()['value']

            return [
                item['ID'] for item in Response if (item['ID'] != '2017-May-B')
            ]
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist während der API Request aufgetreten: {e}")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None
