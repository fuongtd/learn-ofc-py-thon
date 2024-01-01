import requests
import json
import time
import random 

# Register the azure app first and make sure the app has the following permissions:
# files: Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user: User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail: Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# After registration, you must click on behalf of xxx to grant administrator consent, otherwise outlook api cannot be called






calls = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/beta/me/outlook/masterCategories',
    'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]


def get_access_token(refresh_token, client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    html = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    return access_token

def main():
    random.shuffle(calls)
    endpoints = calls[random.randint(0, 10)::]
    access_token = get_access_token(refresh_token, client_id, client_secret)
    session = requests.Session()
    session.headers.update({
        'Authorization': access_token,
        'Content-Type': 'application/json'
    })

    num = 0
    content_to_write = ''  # Biến để lưu trữ nội dung để ghi vào tệp

    for endpoint in endpoints:
        try:
            response = session.get(endpoint)
            status_code = response.status_code

            # In ra yêu cầu API kèm status code
            print(f'{num}th Call to {endpoint} - Status code: {status_code}')

            # Thêm nội dung vào biến content_to_write
            content_to_write += f'{num}th Call to {endpoint} - Status code: {status_code}\n'

            if status_code == 200:
                num += 1
        except requests.exceptions.RequestException as e:
            print(e)
            pass

    localtime = time.asctime(time.localtime(time.time()))
    print('The end of this run is:', localtime)
    print('Number of calls is:', str(len(endpoints)))

    # Ghi nội dung vào tệp test.py
    with open('test.py', 'a') as file:
        file.write(content_to_write)

for _ in range(2):
    main()
