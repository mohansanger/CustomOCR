import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "https://devlpoment.cognitiveservices.azure.com/"
key = "51ncnG30FnzJIceBUHyF6rDM9MPJDmUy04tS4iEbxCLLIkQzTgiRJQQJ99ALACYeBjFXJ3w3AAALACOG4h7r"
path=r"E:\AzureOCRCustomCode\Samples\2.pdf"
polygon = [1.5231, 4.2749, 2.2847, 4.2749, 2.2847, 4.4671, 1.5231,4.4671]
polygon=[round(num,1) for num in polygon]

def extract_text_from_polygon(endpoint, key, path, polygon):
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    with open(path, "rb") as file:
        poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=file)
        result = poller.result()
    result_dict = result.to_dict()
    
    extracted_text = ""
    
    for page in result_dict.get('pages', []):
        for line in page.get('lines', []):
            print(line.get('content'))
            line_polygon = line.get('polygon') 
            converted_list = [] 
            for item in line_polygon: 
                converted_list.append(item['x']) 
                converted_list.append(item['y'])
            converted_list=[round(num,1) for num in converted_list]
            if converted_list == polygon:
                extracted_text += line.get('content') + " " 
    return extracted_text 
   



extracted_text = extract_text_from_polygon(endpoint, key, path, polygon)
print("Extracted Text:", extracted_text)
