from bs4 import BeautifulSoup
import re
import os
import sys
import yaml
from yaml.loader import SafeLoader
from pprint import pprint 


def extract_junos_range(string):
    junos_segments = []

    # for example: 21.4 versions prior to 21.4R1-S1
    junos_template = "\d{2}\.\d{1}[^\r\n\t\f\v, ]*"
    if match := re.match(fr'({junos_template}) versions prior to ({junos_template})', string):
        junos_segments.append([match.group(1), match.group(2)]) 

    # for example: All versions 17.3R1 and later versions prior to 19.2R3-S5
    elif match := re.match(fr'All versions ({junos_template}) and later versions prior to ({junos_template})', string):
        junos_segments.append([match.group(1), match.group(2)]) 

    # for example: 16.1 versions 16.1R7-S6 and later versions prior to 16.1R7-S8
    elif match := re.match(fr'({junos_template}) versions ({junos_template}) and later versions prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: 13.2 version 13.2R1 and later versions prior to 15.1R7-S11
    elif match := re.match(fr'({junos_template}) version ({junos_template}) and later versions prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: 17.2 version 17.2R2 and later prior to 17.2R3-S2
    elif match := re.match(fr'({junos_template}) version ({junos_template}) and later prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: 20.1 version 20.1R1 and later versions
    elif match := re.match(fr'({junos_template}) version ({junos_template}) and later versions', string):
        junos_segments.append([match.group(2), "100.0"]) 

    # for example: 16.1 versions starting from 16.1R6 and later releases, including
    #  the Service Releases, prior to 16.1R6-S6, 16.1R7-S3
    elif match := re.match(fr'({junos_template}) versions starting from ({junos_template}) and later releases, including the Service Releases, prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: 17.2 versions starting from 17.2R1-S3, 17.2R3 and later releases,
    #  including the Service Releases, prior to 17.2R3-S1
    elif match := re.match(fr'({junos_template}) versions starting from ({junos_template}), ({junos_template}) and later releases, including the Service Releases, prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(4)]) 

    # for example: 15.1X49 versions 15.1X49-D100 and above, but prior to 15.1X49-D121
    elif match := re.match(fr'({junos_template}) versions ({junos_template}) and above, but prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: 12.3X48 versions 12.3X48-D55 and above but prior to 12.3X48-D65
    elif match := re.match(fr'({junos_template}) versions ({junos_template}) and above but prior to ({junos_template})', string):
        junos_segments.append([match.group(2), match.group(3)]) 

    # for example: All versions prior to and including 12.3
    elif match := re.match(fr'All versions prior to and including ({junos_template})', string):
        junos_segments.append(["0.0", match.group(1)]) 

    # for example: All versions prior to 12.3R12-S21
    elif match := re.match(fr'All versions prior to ({junos_template})', string):
        junos_segments.append(["0.0", match.group(1)]) 

    # for example: , 18.4R3-S9
    for match in re.findall(fr', ({junos_template})', string):
        junos_segments.append([match, match]) 
        
    return junos_segments


def string_filter(string):
    if re.match(r'(\d{2}\.\d{1}\S*|All) version', string.strip()) and 'EVO' not in string \
        and 'Evolved' not in string and 'except' not in string and 'exceptions' not in string:
            return string.strip().rstrip(".,;")
    return ""


def affected_platforms(string):
    all_platforms = ['vMX', 'MX', 'EX', 'vSRX', 'SRX', 'QFX', 'NFX', 'ACX', 'QFabric', 'Space']
    return re.findall("|".join(all_platforms), string)

    
def find_severity(strings):
    severity = 'None'
    lst = list(strings)
    for i, v in enumerate(lst):
        if v == "Severity":   
            if lst[i + 1]:
                severity = lst[i + 1]
            break  
    return severity


def find_platforms(strings, input_platforms):
    platforms = set() 
    for string in strings:
        if string == "Solution":
            break
        platforms.update(affected_platforms(string))
    if platforms:
        return list(set(platforms) & set(input_platforms))
    else:
        return input_platforms
        
        
def find_junos_ranges(strings):
    junos_ranges = list()
    for strng in strings:
        for string in strng.split(";"):
            if string := string_filter(string):
                for junos_range in extract_junos_range(string):
                    junos_ranges.append(junos_range)    
    return junos_ranges 


def find_cves(html_tags):
    cves = set()
    cves.update(re.findall(r'CVE-\d+-\d+', html_tags))  
    # for html_tag in html_tags:
    #     cves.update(re.findall(r'CVE-\d+-\d+', html_tag.text))
    return cves

def find_tags():
    return ['tag', 'tag']


class BaseParser:
    def __init__(self, config):
        self.sources = config['sources']
        self.platforms = config['platforms']
        self.cve_template = config['cve_template']
        self.cve_db = []
        
    def start(self): 
        cve_counter_base = dict()
        self.cve_db.clear()    
        for file in os.listdir(self.sources):
            if file.endswith('.html'):
                with open(f"{self.sources}/{file}") as obj:
                    soup = BeautifulSoup(obj, 'html.parser')
                    severity = find_severity(soup.strings)
                    platforms = find_platforms(soup.strings, self.platforms)          
                    junos_ranges = find_junos_ranges(soup.strings)
        
                    html_tags = soup.find_all(text = True)  
                    cves = find_cves(file)
                    tags = find_tags()
                    for cve in cves:
                        # if cve not in cve_counter_base:
                        #     cve_counter_base[cve] = 1
                        # else:
                        #     cve_counter_base[cve] = cve_counter_base[cve] + 1
                                # 'name': str(f"{cve}#{cve_counter_base[cve]}"),
                        
                            cve_obj = {
                                'name': str(cve),
                                'severity': str(severity),
                                'url': str(file),
                                'platforms': platforms.copy(),
                                'affected_junos': junos_ranges.copy(),  
                                'tags': tags.copy()
                            }   
                            self.cve_db.append(cve_obj.copy())    
   
if __name__ == "__main__":
    argv = sys.argv[1:]
    config_file = argv[0]
    input_data = dict()
    with open(config_file) as file:
        input_data = yaml.load(file, Loader=SafeLoader)
    
    bp = BaseParser(input_data)
    bp.start()
    pprint(bp.cve_db)
                    