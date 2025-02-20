import string
import requests
from SetGlobalVariables import *
import re
from bs4 import BeautifulSoup
import json

def getMsrcDownloadDialog(
        id : string
) -> None:
    """
    Get the downloadlink from the downloadialog

    Calls the Microsoft Catalog DownloadDialog

    Returns:
        Returns None or prints an error message if the catalog call fails.

    Examples:
        getMsrcDownloadDialog(id)
    """
    url = f"https://catalog.update.microsoft.com/DownloadDialog.aspx"

    _Headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Host': 'catalog.update.microsoft.com',
    'Origin': 'https://catalog.update.microsoft.com',
    'Referer': 'https://catalog.update.microsoft.com/DownloadDialog.aspx',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    _Body = {
    'updateIDs': f'[{{"size":0,"languages":"","uidInfo":"{id}","updateID":"{id}"}}]',
    'updateIDsBlockedForImport': '',
    'wsusApiPresent': '',
    'contentImport': '',
    'sku': '',
    'serverName': '',
    'ssl': '',
    'portNumber': '',
    'version': ''
}
    
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

    try:
        if id is not None :
            response = requests.post(url, headers=_Headers, data=_Body, auth=_Auth, proxies=_Proxies)
            print(f"Headers: {_Headers}")
            print(f"Body (data): {_Body}")
            soup = BeautifulSoup(response.content, 'html.parser')
            html_string = soup.prettify()

            pattern = r"downloadInformation\[0\]\.files\[0\]\.url\s*=\s*'([^']+)'"
            match = re.search(pattern, html_string)

            if match:
                return match.group(1)

            print(s)
        else :
            raise ValueError("Keine ID für Web Request erhalten")

    except requests.exceptions.HTTPError as e :
        print(f"HTTP Get failed mit status code {response.status_code}: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist während der API Request aufgetreten: {e}")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None