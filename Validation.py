import re
valid_nationalities = [ "American", "British", "Canadian", "French", "German", "Indian", "Japanese", "Chinese", "Australian", "Brazilian" ]
valid_place_of_issue=["NEW DELHI","AHMEDABAD"]

def validate_nationality(nationality):
    if nationality is None:
        return False
    nationality=nationality.title()
    if nationality in valid_nationalities:
        return True
    else:
        return False
def validate_adharcard_number(str1):
    match=re.findall(r'[0-9]{4}\s[0-9]{4}\s[0-9]{4}',str1)
    if match:
        return True
    else:
        return False
def validate_Date(str1):
    #date=31 / 12 / 2022
    #pattern=r'^([0-2][0-9]|3[0-1])\s/\s(0[1-9]|1[0-2])\s/\s(19|20)\d{2}$'
    dat=re.sub(r'\s+','',str1)     
    match=re.findall(r'^(0[0-9]|[12][0-9]|3[01])/(0[0-9]|1[0-2])/([0-9]{4})$',dat)
    if match:
        return True
    else:
        return False

def validate_place_of_issue(placeofissue):
    if placeofissue is None:
        return False
    #placeofissue=placeofissue.title()
    if placeofissue in valid_place_of_issue:
        return True
    else:
        return False