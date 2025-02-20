import os
import requests
from SetGlobalVariables import *
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from GetMsrcDownloadDialog import getMsrcDownloadDialog

def getMsrcDownload(
        downloadLinks : set
) -> None:
    """
    Get all downloads.

    Calls the Microsoft catalog to download upadates.

    Returns:
        Returns None or prints an error message if the catalog call fails.

    Examples:
        getMsrcDownload(example)
    """

    _Headers = {'Accept': 'application/xml'}
    
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
        if downloadLinks is not None :
            
            for url in downloadLinks :
                response = requests.post(url, headers=_Headers, auth=_Auth, proxies=_Proxies)

                soup = BeautifulSoup(response.content, 'html.parser')
                html_string = soup.prettify()
                inputElements = soup.find_all(class_='flatBlueButtonDownload focus-only')

                for inputElement in inputElements :
                    id = inputElement.attrs["id"]
                    downloadUrl = getMsrcDownloadDialog(id) 
                    if downloadUrl:
                        file_name = downloadUrl.replace('/', '').replace('\\', '').replace(':', '').replace('"', '').replace('?', '').replace('<', '').replace('>', '').replace('*', '').replace('|', '')
                        folder_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

                        try:
                            response = requests.get(downloadUrl, stream=True, allow_redirects=True)
                            response.raise_for_status()
                            with open(folder_path, 'wb') as file:
                                for chunk in response.iter_content(chunk_size=8192):
                                    file.write(chunk)
                            print(f"Installiert: {folder_path}")
                        except requests.exceptions.RequestException as e:
                            print(f"Download error: {e}")
                    else:
                        print(f"Kein Download für die ID: {id}")

        else :
            raise ValueError("Keine Downloadlinks erhalten.")

    except requests.exceptions.HTTPError as e :
        print(f"HTTP Get failed mit status code {response.status_code}: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist während der API Request aufgetreten: {e}")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None