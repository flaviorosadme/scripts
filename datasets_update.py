import requests
import json
import sys
import shlex

def create_session():
	return requests.Session()

def close_session():
    session.close()

def organization_list(session, ckan_url, api_key):
    
    headers = {
        'Cache-Control': 'no-store'
    }
    group_rst = session.get(
        ckan_url + '/api/action/organization_list', headers=headers, verify=False)

    return group_rst.json()['result']


def show_dataset(session, dataset_id):
	#Show dataset function
	dataset = session.get(ckan_url + '/api/action/package_show', params = dataset_id)
	return dataset.json()['result']
	
def show_dataset_list(session, organization):
	headers = {'Cache-Control':'no-store'}
	params = {'q': organization}
	dataset_list=session.get(ckan_url + '/api/action/package_search', headers = headers, params = params)
	return dataset_list.json()['result']['results']
	
def update_resources_url(session, dataset_id, api_key, old_url, new_url):
	"""Update of a dataset"""
	headers = {
		'Content-Type':'application/json',
		'Authorization': api_key
		}
	
	dataset = show_dataset(session, dataset_id)
	for i in range(0,len(dataset['resources'])):
		dataset['resources'][i]['url'] = dataset['resources'][i]['url'].replace( old_url , new_url)
	update = session.post(ckan_url + '/api/action/package_update',
	json=dataset,
	headers=headers)
	
	return update.json()['result']
	
def update_dataset(session,api_key,ckan_url,organization,old_url,new_url):
	if organization not in organization_list(session, ckan_url, api_key):
		print("The organization does not exist, please try again.")
		close_session() 
		sys.exit()
	
	dataset_list = show_dataset_list(session,organization)
	for dataset in dataset_list:
		dataset_id = {'id' : dataset['id']}
		updated_dataset = update_resources_url(session, dataset_id, api_key, old_url, new_url)
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
		organization = args[2]
		old_url = args[3]
		new_url = args[4]
		
    	except Exception as e:
		print("Exception: " + str(e) + "\n")
		print help_msg
		sys.exit()
	
	#api_key = '110e1090-edd4-453e-b106-ef00d76b78a9'

	#ckan_url = 'http://localhost:5000'
	
	#organization = 'simocean' 

	#old_url='http://catalogue.simocean.pt'
	
	#new_url='https://simocean.store4EO.com'
	
	session = create_session()
	update_dataset(session,api_key,ckan_url,organization,old_url,new_url)
	close_session() 


''''''
