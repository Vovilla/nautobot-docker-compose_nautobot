import uuid
import sys
import yaml
import httpx
import re
from yaml.loader import SafeLoader
from base_parser import BaseParser
from pprint import pprint

# myuuid = uuid.uuid4()

# print(str(myuuid))

class JunOS:
    def __init__(self, string):
        string = re.sub('x', '0', string)
        self.string = string
        main_and_minor = 0
        release = 0
        release_spin = 0
        service = 0
        service_respin = 0      
        if "R" in string or "F" in string:
            self.type = "R"
        elif "X" in string:
            self.type = "X"
        string_split_list = re.split("R|X|F|-S|-D", string)
        main_and_minor = float(string_split_list[0])
        if len(string_split_list) == 1:
           self.type = "R" 
        if len(string_split_list) == 2:
            release_split_list = string_split_list[1].split(".")
            # 12.3R case
            if release_split_list[0]:
                release = int(release_split_list[0])
            else:
                release = 0
            if len(release_split_list) == 2:
                release_spin = int(release_split_list[1])
        if len(string_split_list) == 3:
            release = int(string_split_list[1])
            service_split_list = string_split_list[2].split(".")
            service = int(service_split_list[0])
            if len(service_split_list) == 2:
                service_respin = int(service_split_list[1])                               
        self.data = (main_and_minor, release, service, service_respin, release_spin)

    def __le__(self, other):
        if self.type == other.type:
            return self.data <= other.data
        else:
            return False

    def __ge__(self, other):
        if self.type == other.type:
            return self.data >= other.data
        else:
            return False

argv = sys.argv[1:]
config_file = argv[0]
input_data = dict()
with open(config_file) as file:
    input_data = yaml.load(file, Loader = SafeLoader)
    
bp = BaseParser(input_data)
bp.start()

access_token = '0123456789abcdef0123456789abcdef01234567'
headers = {
    'Authorization': f"Token {access_token}",
    'Content-Type': 'application/json',
    'Accept': 'application/json; indent=4'
}

for cve_db_entry in bp.cve_db:
    ids = []    
    response = httpx.get('http://localhost:8080/api/plugins/nautobot-device-lifecycle-mgmt/software/', headers = headers)
    softwares = (response.json())['results']
    # JunOS(software['version']) >= JunOS(affected_junos[0]) and \
    #             JunOS(software['version']) <= JunOS(affected_junos[1])
    for software in softwares:
        for affected_junos in cve_db_entry['affected_junos']:
            if True:
                ids.append({"id": software['id']})
                break
    cve_data = {
        'name': cve_db_entry['name'],
        'severity': cve_db_entry['severity'],
        'published_date': '2022-11-25',
        'link': 'http://link.com',
        "relationships": {
            "soft_cve": {
                "source": {
                    "objects": [ids[0]]
                }
            }
        }
    }
    cve_id = ''
    try:
        response = httpx.post('http://localhost:8080/api/plugins/nautobot-device-lifecycle-mgmt/cve/', headers = headers, json = cve_data)
        cve_id = (response.json())['id']
    except:
        continue
    for software in softwares:
        for affected_junos in cve_db_entry['affected_junos']:
            if True:
                software_data = {
                    "device_platform": software['device_platform']['id'],
                    "version": software['version'],
                    'link': 'http://link.com',
                    "relationships": {
                        "soft_cve": {
                            "source": {
                                "objects": [
                                    {
                                        "id": cve_id
                                    }     
                                ]
                            }
                        }
                    }
                }
                response = httpx.put(f"http://localhost:8080/api/plugins/nautobot-device-lifecycle-mgmt/software/{software['id']}/", headers = headers, json = software_data)
                break
    

# class httpx_wrapper(httpx):

    


#   "alias": "string",
#   "release_date": "2022-11-25",
#   "end_of_support": "2022-11-25",
#   "documentation_url": "string",
#   "software_images": [
#     "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#   ],
#   "long_term_support": true,
#   "pre_release": true,
#   "custom_fields": {},
#   "tags": [
#     {
#       "name": "string",
#       "slug": "string",
#       "color": "string"
#     }
#   ]
  
  
# # post software. Для создания software можно не использовать software_image!!!
# {
#   "device_platform": "2f1206eb-7c5c-4203-9240-85dfdbe390a8",
#   "version": "17.1R1.1"
# }


# # post cve
# {
#   "name": "CVE111",
#   "published_date": "2022-11-25",
#   "link": "http://link.com",
#   "severity": "Critical",
#   "relationships": {
#     "soft_cve": {
#       "source": {
#         "objects": [
#           {
#             "id": "9d94ebeb-4411-4e48-882f-1715c94b378b"
#           }
#         ]
#       }
#     }
#   }
# }

# # put cve to software

# [{'id': 'a6d59612-495f-4712-9df1-f66e01e12483'}, {'id': '10bf579d-82da-4dfd-81f4-380015310ca4'}]