import os
from openai import OpenAI
import time
import uuid
import json
import pandas as pd
import requests
from config import settings

# key
ocr_secret_key = settings.OCR_KEY

# OCR raw 결과
def ocr_request(image_path, secret_key):
    api_url = 'https://37yy63o83d.apigw.ntruss.com/custom/v1/31455/ffa6c9cb9b19c96c7d2619ad2fffdd1a4b228c4b760720a1c3e8a57c2938e8c4/document/receipt'
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', open(image_path, 'rb'))
    ]
    headers = {
        'X-OCR-SECRET': secret_key
    }
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    return response

# OCR 결과를 JSON 파일로 저장
def save_ocr_result(response, output_file):
    if response.status_code == 200:
        result = response.json()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"OCR 결과가 {output_file} 파일로 저장되었습니다.")
        return result
    else:
        print("Error Code:", response.status_code)
        print(response.text)
        return None

# OCR 결과 파싱
def parse_receipt(result):
    items = []
    for sub_result in result['images'][0]['receipt']['result']['subResults']:
        for item in sub_result['items']:
            name = item.get('name', {}).get('text', '')
            count = item.get('count', {}).get('text', '')
            price = item.get('price', {}).get('price', {}).get('text', '')
            items.append({'Item': name, 'Count': count, 'Price': price})
    return items

# 최종 함수
def ocr_to_dataframe(image_path, secret_key, output_file='ocr_result.json'):
    response = ocr_request(image_path, secret_key)
    if response.status_code == 200:
        result = save_ocr_result(response, output_file)
        if result:
            receipt_items = parse_receipt(result)
            ocr_data = pd.DataFrame(receipt_items)
            return ocr_data
    else:
        print("OCR 요청 실패")
        return None

# 사용 예시
if __name__ == "__main__":
    image_file = 'GustomateApp/OCR.jpeg'
    ocr_data = ocr_to_dataframe(image_file, ocr_secret_key)
    if ocr_data is not None:
        print(ocr_data)


# ======================== GPT =======================

client = OpenAI(
    api_key = settings.OPENAI_KEY
)
  
def gpt_extract_ingredient(item):
    prompt = f"다음 제품명을 보고 음식에 들어가는 식재료인지 판단하고, 가장 적절한 식재료명으로 변환해주세요. 이때 브랜드명이나 부수적 표현을 제외하고 가장 일반적인 식재료명으로만 답하세요. 단어 1개로 답하세요: {item}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful Korean assistant identifying food and ingredients name."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )
    extracted_ingredient = response.choices[0].message.content
    return extracted_ingredient

def clean_ocr_data(ocr_data):
    ocr_data['Cleaned Item'] = ocr_data['Item'].apply(gpt_extract_ingredient)
    return ocr_data

# 사용 예시
if __name__ == "__main__":
    secret_key = settings.OPENAI_KEY
    image_file = 'GustomateApp/OCR.jpeg'
    
    ocr_data = ocr_to_dataframe(image_file, ocr_secret_key)
    if ocr_data is not None:
        cleaned_ocr_data = clean_ocr_data(ocr_data)
        print(cleaned_ocr_data)
