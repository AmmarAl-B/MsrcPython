from GetMsrcCvrfDocument import *
from GetMsrcAffectedSoftware import *
from GetMsrcDownload import *

resonse = getMsrcCvrfDocument('2024-Apr')

element = getMsrcAffectedSoftware(resonse)

getMsrcDownload(element)

print(resonse)