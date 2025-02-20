import requests
import json
from SetGlobalVariables import *
from GetCVRFID import getCVRFID

def getMsrcCvrfDocument(
        id : str
) -> json:
    """
    Get a MSRC CVRF document.

    Calls the MSRC CVRF API to get a CVRF document by ID.

    Returns:
        json: CVRF document as JSON
              Returns None and prints an error message if the API call fails.

    Examples:
        getMsrcCvrfDocument ('2016-Aug')
        # Get the Cvrf document '2016-Aug' (returns a CVRF JSON)

    Notes:
        An API Key for the MSRC CVRF API is not required anymore.
    """

    url = f"{msrcApiUrl}/cvrf/{id}?{msrcApiVersion}"

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

    try:
        allCVRFID = getCVRFID()

        if any(ext in id for ext in allCVRFID) :

            Response = requests.get(url, headers=_Headers, auth=_Auth, proxies=_Proxies)
            Response.raise_for_status()

            return Response.json()
        else :
            raise ValueError("Die angegebene CVRFID ist ungültig.")

    except requests.exceptions.HTTPError as e :
        print(f"HTTP Get failed mit status code {Response.status_code}: {Response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist während der API Request aufgetreten: {e}")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None