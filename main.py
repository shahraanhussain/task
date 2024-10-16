import requests
import math
import os
from database import MongoDBManager


class GSFRegistry:
    def __init__(self):
        self.project_ids = []
        self.manager = MongoDBManager("my_database", "my_collection")

    def all_projects(self,page_no='1'):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://registry.goldstandard.org',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://registry.goldstandard.org/',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
        }

        params = {
            'query': '',
            'page': f'{page_no}',
            'size': '150',
            'sortColumn': '',
            'sortDirection': '',
        }

        response = requests.get('https://public-api.goldstandard.org/projects', params=params, headers=headers)
        if response.status_code == 200:
            headers = response.headers
            self.total_entry = headers['x-total-count']
            json_data = response.json()
            for each in json_data:
                project_id = each['id']
                self.project_ids.append(project_id)
            return json_data
        
    def get_project_id_details(self,project_id):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://registry.goldstandard.org',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://registry.goldstandard.org/',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
        }
        response = requests.get(f'https://public-api.goldstandard.org/projects/{project_id}', headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            
            download_url = json_data.get("sustaincert_url","")
            if download_url:
                directory_path = f"./Project-{project_id}"
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                
                download_url_id = download_url.split("/")[-1]
                filename_list = self.get_all_filename(download_url_id)
                filepath_list = []
                for filename in filename_list:
                    download_file = self.download_file(download_url_id,filename,directory_path)
                    filepath_list.append(download_file)
                json_data['filepath_list'] = filepath_list
            insert_document = self.manager.append_document(json_data)
            print(json_data)
                
    
    def get_all_filename(self,download_url_id):
        params = {
            'projectID': f'{download_url_id}',
        }

        response = requests.get(
            'https://sc-platform-certification-prod.azurewebsites.net/api/document/publiclist',
            params=params,
            #headers=headers,
        )
        filename_list = []
        if response.status_code == 200:
            json_data = response.json()
            file_list = json_data['files']
            for each in file_list:
                filename = each['fileName']
                filename_list.append(filename)
        return filename_list       

    def download_file(self,project_id,filename,directory_path):
        response = requests.get(
            f'https://sc-platform-certification-prod.azurewebsites.net/api/document/publicdownload?projectID={project_id}&fileName={filename}'
        )
        if response.status_code == 200:
            complete_path = f"{directory_path}/{filename}"
            with open(complete_path, "wb") as file:
                file.write(response.content)
            return complete_path



                
bot = GSFRegistry()
projects = bot.all_projects()

total_entries = bot.total_entry
max_entries = 150
if total_entries:
    total_pages = math.ceil(int(total_entries)/max_entries)
    print(total_pages)
#for single page

if total_pages > 1:
    for page in range(2,total_pages+1):
        project_ids = bot.all_projects(page)
print(bot.project_ids)
for each in bot.project_ids[:4]:
    project_id_data = bot.get_project_id_details(each)




# print(bot.url_list)
# print(len(bot.url_list))


