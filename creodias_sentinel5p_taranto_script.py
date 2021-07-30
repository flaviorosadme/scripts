def get_data(start_date,end_date, output_format):

  r = requests.get('https://finder.creodias.eu/resto/api/collections/'
                   'Sentinel5P/search.{2}?_pretty=true&q=&'
                   'box=16.48,39.7,18.37,40.75&'
                   'startDate={0}'
                   '&completionDate={1}'.format(start_date,end_date,output_format))
  if output_format == 'json':
  	return r.json()
  if output_format == 'atom':
  	return r.text

if __name__=="__main__":

	help_msg = """
	Usage: $ python creodias_sentinel5p_taranto_script.py <start_date> <end_date>	<format>
<start_date> e.g.: 2020-01-01
<end_date> : e.g.:2020-01-02
<format> e.g.: json or atom
                
	 """	
	
	args = shlex.split(' '.join(sys.argv[1:]))

	if args[0] == '-h':
        	print help_msg
		sys.exit()
	try:
		start_date = args[0]
		end_date = args[1]
		output_format = args[2]
		
    	except Exception as e:
		print("Exception: " + str(e) + "\n")
		print help_msg
		sys.exit()
    
        output = get_data(start_date,end_date, output_format)
        print(output)
