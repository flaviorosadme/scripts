import requests
import json
import sys
import shlex

def create_session():
	return requests.Session()

def close_session():
    session.close()

def collection_id_list(session, ckan_url, api_key):
    
    headers = {
        'Cache-Control': 'no-store'
    }
    group_rst = session.get(
        ckan_url + '/api/action/vocabulary_list', headers=headers, verify=False)
    print(group_rst.json())
    return group_rst.json()['result']


def show_dataset(session, dataset_id):
	#Show dataset function
	dataset = session.get(ckan_url + '/api/action/package_show', params = dataset_id)
	return dataset.json()['result']
	
def show_dataset_list(session,collection_id):
	headers = {'Cache-Control':'no-store'}
	params = {'q': collection_id}
	dataset_list=session.get(ckan_url + '/api/action/package_search', headers = headers, params = params)
	return dataset_list.json()['result']['results']
	
def update_resources_url(session, dataset_id, api_key, old_str, new_str):
	"""Update of a dataset"""
	headers = {
		'Content-Type':'application/json',
		'Authorization': api_key
		}
	
	dataset = show_dataset(session, dataset_id)
	for i in range(0,len(dataset['resources'])):
		dataset['resources'][i]['descritpion'] = dataset['resources'][i]['description'].replace( old_str , new_str)
	update = session.post(ckan_url + '/api/action/package_update',
	json=dataset,
	headers=headers)
	
	return update.json()['result']
	
def update_dataset(session,api_key,ckan_url,collection_id,old_str,new_str):
	'''if collection_id not in collection_id_list(session, ckan_url, api_key):
		print("The collection_id does not exist, please try again.")
		close_session() 
		sys.exit()'''
	
	dataset_list = show_dataset_list(session,collection_id)
	for dataset in dataset_list:
		dataset_id = {'id' : dataset['id']}
		updated_dataset = update_resources_url(session, dataset_id, api_key, old_str, new_str)
	return updated_dataset

if __name__=="__main__":

	help_msg = """
	Usage: $ python datasets_update.py <destination_ckan_apikey> <destination_ckan_URL>	<organization> <old_url> <new_url>
<destination_ckan_URL> e.g.: "https://your-ckan-catalogue"
<destination_ckan_apikey> : get the API Key of your CKAN admin user"
<organization> e.g.: simocean
<old_url> e.g.: "https://old-resource-url"
<new_url> e.g.: "https://new-resource-url"
                
	 """	
	
	args = shlex.split(' '.join(sys.argv[1:]))

	if args[0] == '-h':
        	print help_msg
		sys.exit()
	try:
		api_key = args[0]
		ckan_url = args[1]
		collection_id = args[2]
		old_str = args[3]
		new_str = args[4]
		
    	except Exception as e:
		print("Exception: " + str(e) + "\n")
		print help_msg
		sys.exit()
	
	#api_key = 'ec99a15a-a087-4d10-8f47-9ed627a57619'

	#ckan_url = 'https://catalogue-staging.nextgeoss.eu'
	
	#collection_id = 'simocean' 

	#old_str='NOTE: DOWNLOAD REQUIRES LOGIN'
	
	#new_str=''
	
	session = create_session()
	#print(show_dataset_list(session,'FSSCAT_FMP_L4__SIT'))
	update_dataset(session,api_key,ckan_url,collection_id,old_str,new_str)
	close_session() 


''''''
