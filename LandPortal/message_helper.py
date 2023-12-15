import aiohttp
import json
from flask import current_app
import requests

async def send_message(data):
    with open('config.json') as config_file:
        config = json.load(config_file)
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }
    
    async with aiohttp.ClientSession() as session:
        url = 'https://graph.facebook.com' + f"/{config['VERSION']}/{config['PHONE_NUMBER_ID']}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)        
                    print(response)        
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))

#application/pdf
#application/vnd.ms-excel
def upload_media(file_path, media_type):
    with open('config.json') as config_file:
        config = json.load(config_file)
    headers = {
       # "Content-type": "application/json",
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }
    
    url = 'https://graph.facebook.com' + f"/v17.0/{config['PHONE_NUMBER_ID']}/media"
    files = {'file': (file_path, open(file_path, 'rb'), media_type, {'Expires': '0'})}

    data = {
        #'files':{'file': (file_path, open(file_path, 'rb'), media_type, {'Expires': '0'})},
        'messaging_product': 'whatsapp',
        'type': media_type
    }
    print(data['messaging_product'])
    response = requests.post(url, data = data, files = files, headers = headers)
    return response.json()

def get_media_url(media_id):
    with open('config.json') as config_file:
        config = json.load(config_file)
    headers = {
       # "Content-type": "application/json", #maybe remove in both functions
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }
    url = 'https://graph.facebook.com' + f"/v17.0/{media_id['id']}/"
    media_url = requests.get(url, headers = headers)['url']
    print(media_url)
    response = requests.get(media_url, headers=headers)
    return response
    #return response.json()

def get_text_message_input(recipient, text):
  return json.dumps({
    "messaging_product": "whatsapp",
    "preview_url": False,
    "recipient_type": "individual",
    "to": recipient,
    "type": "text",
    "text": {
        "body": text
    }
  })
  
def get_templated_message_input(recipient, parameters, link, filetype):
  return json.dumps({
    "messaging_product": "whatsapp",
    "to": recipient,
    "type": "template",
    "template": {
      "name": "land_search",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "document",
              "document": {
                "filename": "results." + filetype,
                "link": link
              }
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": parameters['District']
            },
            {
              "type": "text",
              "text": parameters['Tehsil']
            },
            {
              "type": "text",
              "text": parameters['Village']
            },
            {
              "type": "text",
              "text": parameters['Land Type']
            },
            {
              "type": "text",
              "text": parameters['Minimum Area']
            }
          ]
        }
      ]
    }
  })