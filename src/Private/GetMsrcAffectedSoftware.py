import json

def getMsrcAffectedSoftware (
        documentJSON : json
) -> set :
        """
    Get download URLs of products affected by a CVRF document.

    Retrieves all necessary information from the CVRF json.

    Returns:
        list: A list of URLs for furhter processing.
              Returns None and prints an error message if the API call fails.

    Examples:
        result = GetMsrcCvrfDocument ('2016-Aug')
        # Get the Cvrf document '2016-Aug' (returns a dictionary converted from the CVRF JSON)

        GetMSrcAffectedSoftware(result)
    """
        try :
               
                if documentJSON is None:
                    raise ValueError("Das übergebene Dokument ist leer")
                
                _listWindowsUpdates = []
                for productName in documentJSON['ProductTree'].get('FullProductName') :
                        if 'Windows 10' in productName.get('Value') :
                            _listWindowsUpdates.extend(productName.get('ProductID').split("-"))


                return {
                    remediation.get('URL')
                    for vulnerability in documentJSON['Vulnerability']
                    for remediation in (vulnerability.get('Remediations') or [])
                    if remediation.get('Type') == 2 and remediation.get('URL') != "" and remediation.get('ProductID')[0] in _listWindowsUpdates
                }

        except Exception as e:
                print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
                return None