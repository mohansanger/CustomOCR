
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import csv
from dotenv import load_dotenv
import os
import json
import Validation 

load_dotenv()


endpoint = "https://devlpoment.cognitiveservices.azure.com/"
key = "51ncnG30FnzJIceBUHyF6rDM9MPJDmUy04tS4iEbxCLLIkQzTgiRJQQJ99ALACYeBjFXJ3w3AAALACOG4h7r"
#endpoint=os.getenv('AzureEndPoint')
path=r"E:\AzureOCRCustomCode\Samples\1.pdf"


def analyze_read():
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    file= open(path, "rb")
    poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=file )
    result = poller.result()
      
    for page in result.pages:
        for line_idx, line in enumerate(page.lines):
       #_________________________Extracted AADHAAR NUMBER From Multi Line__________________________________
            if line.content == "AADHAAR NUMBER":              
                polygonThreshold=0.2 #0.2 #addition of two coordinate from 1st element position 0(y) and Element 2nd position 0(y)
                e1c1x=line.polygon[0][1]
                AdharCardNo=findNextElement_y_coordinate(page.lines,polygonThreshold,line_idx,e1c1x) # element in the next line based on y coordinate
                is_vlaid_flag=Validation.validate_adharcard_number(AdharCardNo)
                if is_vlaid_flag !=True:
                    polygonThreshold=0.8
                    AdharCardNo=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                    is_vlaid_flag=Validation.validate_adharcard_number(AdharCardNo)
                if is_vlaid_flag !=True:
                    print(f"AdharCardNo: {is_vlaid_flag}")
                else:
                    print(f"AdharCardNo: {AdharCardNo}")    
                e1c1x=None
        #___________________Extracted Full Name From Single Line------------------        
            if line.content == "FULL NAME":              
                polygonThreshold=1.1626 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                Name=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"FULL NAME: {Name}")
                #~~~~~~~~~~~~~~~~~~~~~~~Find Date if Birth~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                polygonThreshold=0.5
                e1c1x=line.polygon[0][1]
                line_idx=line_idx+1
                DOB=findNextElement_y_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_Date(DOB)
                if is_vlaid_flag !=True: 
                    print(f"Date Of Birth: {is_vlaid_flag}")
                else:
                    print(f"DATE OF BIRTH: {DOB}")
                e1c1x=None
        #___________________Extracted DOB From Single Line------------------        
            if line.content == "DATE OF BIRTH":              
                polygonThreshold=1.8702 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                DOB=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_Date(DOB)
                if is_vlaid_flag !=True:
                    DOB=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                    is_vlaid_flag=Validation.validate_Date(DOB)
                if is_vlaid_flag !=True: 
                    print(f"Date Of Birth: {is_vlaid_flag}")
                else:
                    print(f"DATE OF BIRTH: {DOB}")
                #~~~~~~~~~~~~~~~~~~~~~~Nationality Extraction using Date of Birth~~~~~~~~~~~~~~~~~~~~~~
                polygonThreshold=1.5
                e1c1x=line.polygon[0][0]
                line_idx=line_idx-1
                Nationality=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_nationality(Nationality)
                if is_vlaid_flag !=True: 
                    print(f"NATIONALITY: {is_vlaid_flag}")
                else:
                    print(f"NATIONALITY: {Nationality}")
                e1c1x=None
        #___________________Extracted Nationality From Single Line------------------        
            if line.content == "NATIONALITY":
                polygonThreshold=1.1
                e1c1x=0.3505
                Nationality=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_nationality(Nationality)               
                
                if is_vlaid_flag !=True:
                    polygonThreshold=1.8736 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                Nationality=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_nationality(Nationality)
                
                if is_vlaid_flag !=True: 
                    print(f"Nationality: {is_vlaid_flag}")
                else:
                    print(f"Nationality: {Nationality}")
                e1c1x=None
        #___________________Extracted Gender From Single Line------------------        
            if line.content == "SEX":              
                polygonThreshold=9.9736 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                Gender=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"Gender: {Gender}")
                e1c1x=None
        #___________________Extracted State Code From Single Line------------------        
            if line.content == "STATE CODE":              
                polygonThreshold=6.4 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                StateCode=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"STATE CODE: {StateCode}")
                e1c1x=None
        #___________________Extracted DATE OF ISSUE From Single Line------------------        
            if line.content == "DATE OF ISSUE":              
                polygonThreshold=1.8 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                DOI=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_Date(DOI)
                if is_vlaid_flag !=True:
                    DOI=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                    is_vlaid_flag=Validation.validate_Date(DOI)
                if is_vlaid_flag !=True: 
                    print(f"Is the DATE OF ISSUE '{DOI}' valid ? {is_vlaid_flag}")
                else:
                    print(f"DATE OF ISSUE: {DOI}")
                e1c1x=None
        #___________________Extracted DATE OF EXPIRY From Single Line------------------        
            if line.content == "DATE OF EXPIRY":              
                polygonThreshold=1.2#1.9 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                DOE=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_Date(DOE)
                if is_vlaid_flag !=True:
                    DOE=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                    is_vlaid_flag=Validation.validate_Date(DOE)
                if is_vlaid_flag !=True: 
                    print(f"Is the DATE OF EXPIRY '{DOE}' valid ? {is_vlaid_flag}")
                else:
                    print(f"DATE OF EXPIRY: {DOE}")
                e1c1x=None
        #___________________Extracted PLACE OF ISSUE From Single Line------------------        
            if line.content == "PLACE OF ISSUE":              
                polygonThreshold=1.9 #1.9#addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                POI=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_place_of_issue(POI)
                #polygonThreshold=2.6
                #e1c1x=line.polygon[1][0]
                #DOE=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                if is_vlaid_flag !=True: 
                    print(f"PLACE OF ISSUE:{is_vlaid_flag}")
                else:
                    print(f"PLACE OF ISSUE: {POI}")
                e1c1x=None
        
        #___________________Extracted DATE OF EXPIRY From Single Line------------------        
            if line.content == "CARD NUMBER":              
                polygonThreshold=1.9 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=line.polygon[0][0]
                CardNumber=findNextElement_x_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"CardNumber: {CardNumber}")
                e1c1x=None
         #___________________Extracted PERMANENT ADDRESS From Single Line------------------        
            if line.content == "PERMANENT ADDRESS":              
                polygonThreshold=0.6 #addition of two coordinate from 1st element position 0(y) and Element 2nd position 0(y)
                e1c1x=line.polygon[0][1]
                ParmenanatAddress=findNextElement_y_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"Address: {ParmenanatAddress}")
                e1c1x=None
        #___________________Extracted Issue Authority From Single Line------------------        
            if line.content == "ISSUING AUTHORITY":              
                polygonThreshold=0.4
                e1c1x=line.polygon[0][1]
                IssueAuth=findNextElement_y_coordinate(page.lines,polygonThreshold,line_idx,e1c1x)
                print(f"ISSUING AUTHORITY: {IssueAuth}")
                polygonThreshold=1.9 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=None
            #___________________Extracted PLACE OF ISSUE From Single Line using Issue Authority------------------        
            if line.content == "ISSUING AUTHORITY":              
                polygonThreshold=1.9 #addition of two coordinate from 1st element position 0(x) and Element 2nd position 0(x)
                e1c1x=1.5
                #e1c1x=line.polygon[0][0]
                POI=findElementValidation_False(page.lines,polygonThreshold,line_idx,e1c1x)
                is_vlaid_flag=Validation.validate_place_of_issue(POI)
                if is_vlaid_flag !=True: 
                    print(f"PLACE OF ISSUE:{is_vlaid_flag}")
                else:
                    print(f"PLACE OF ISSUE: {POI}")
                e1c1x=None

#____________________Function to extract elements from x axis___________________ 
def findElementValidation_False(page_lines, polygonThreshold, line_idx, e1c1x):
        for nxtline in page_lines[line_idx-1:]: 
            e2c1x = nxtline.polygon[0][0] 
            if e1c1x < e2c1x < e1c1x + polygonThreshold:
                return nxtline.content
        return None

#____________________Function to extract elements from x axis___________________ 
def findNextElement_x_coordinate(page_lines, polygonThreshold, line_idx, e1c1x):
        for nxtline in page_lines[line_idx+1:]: 
            e2c1x = nxtline.polygon[0][0] 
            if e1c1x < e2c1x < e1c1x + polygonThreshold:
                return nxtline.content
        return None

#____________________Function to extract elements from y axis___________________ 
def findNextElement_y_coordinate(page_lines, polygonThreshold, line_idx, e1c1x):
        Field1=""
        for nxtline in page_lines[line_idx+1:]: 
            e2c1x = nxtline.polygon[0][1] 
            if e1c1x < e2c1x < e1c1x + polygonThreshold:
                Field=nxtline.content
                Field1=Field1 + Field + ' '
            else:
                break
        return str.strip(Field1)
         

if __name__ == "__main__":
      analyze_read()


