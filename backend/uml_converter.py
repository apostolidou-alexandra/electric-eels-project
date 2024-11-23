import zlib
import base64
import urllib.parse
import requests
import string

import six

if six.PY2:
    from string import maketrans
else:
    maketrans = bytes.maketrans

def encode_plantuml(text):

    plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))

    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')

def generate_uml_diagram(uml_text):
    base_url = "http://www.plantuml.com/plantuml/png/"
    encoded_text = encode_plantuml(uml_text)
    diagram_url = f"{base_url}{encoded_text}"
    return diagram_url

# uml_text = """
# @startuml

# package "rufus" {
#     class "MainWindow" {
#         + void main()
#         + void logMessage()
#         + void startOperation()
#         + void showProgress()
#     }
    
#     class "ISOHandler" {
#         + boolean loadISO(String path)
#         + boolean validateISO()
#         + String getChecksum()
#     }
    
#     class "DriveManager" {
#         + void listDrives()
#         + boolean formatDrive(String drive)
#         + boolean writeISO(String drive, ISOHandler iso)
#     }
    
#     class "FileSystemHelper" {
#         + boolean format(String drive, String fileSystemType)
#         + boolean validate(String drive)
#     }
    
#     class "Settings" {
#         + void loadSettings()
#         + void saveSettings()
#         + String get(String key)
#     }

#     MainWindow "1" *-- "1" ISOHandler
#     MainWindow "1" *-- "1" DriveManager
#     MainWindow "1" *-- "1" Settings
#     DriveManager "1" *-- "1" FileSystemHelper
# }

# @enduml
# """


# diagram_url = generate_uml_diagram(uml_text)
# print("UML Diagram URL:", diagram_url) 