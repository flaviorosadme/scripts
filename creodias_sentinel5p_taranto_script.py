import requests

start_date=raw_input('Start Date(yyyy-mm-dd): ')
end_date=raw_input('\nEnd Date(yyyy-mm-dd): ')


r = requests.get('https://finder.creodias.eu/resto/api/collections/'
                 'Sentinel5P/search.json?_pretty=true&q=&'
                 'box=16.48,39.7,18.37,40.75&'
                 'startDate={0}'
                 '&completionDate={1}'.format(start_date,end_date))
print(r.json())
