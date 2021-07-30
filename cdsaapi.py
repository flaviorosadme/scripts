import cdsapi
import datetime
import sys
import shlex


def cdsaapi(in_start_date,in_end_date):
	start_date=datetime.datetime.strptime(in_start_date, '%Y-%m-%d')
	start_date=start_date.date()

	end_date=datetime.datetime.strptime(in_end_date, '%Y-%m-%d')
	end_date=end_date.date()

	delta=datetime.timedelta(1)

	c = cdsapi.Client()

	while start_date <= end_date:
		c.retrieve(
		    'cams-europe-air-quality-forecasts',
		    {
			'model': 'ensemble',
			'date': '{0}/{1}'.format(start_date,start_date+delta),
			'format': 'netcdf',
			'type': 'analysis',
			'time': '00:00',
			'leadtime_hour': '0',
			'area': [
			    40.75, 16.48, 39.7,
			    18.37,
			],
			'level': '50',
			'variable': [
			    'ammonia', 'carbon_monoxide', 'dust',
			    'nitrogen_dioxide', 'nitrogen_monoxide', 'non_methane_vocs',
			    'ozone', 'particulate_matter_10um', 'particulate_matter_2.5um',
			    'peroxyacyl_nitrates', 'pm10_wildfires', 'pm2.5_anthropogenic_fossil_fuel_carbon',
			    'pm2.5_anthropogenic_wood_burning_carbon', 'residential_elementary_carbon', 'secondary_inorganic_aerosol',
			    'sulphur_dioxide', 'total_elementary_carbon',
			],
		    },
		    'download.nc')
		print(start_date)
		start_date=start_date+delta
	return 0
	
	
if __name__=="__main__":

	help_msg = """
	Usage: $ python cdsaapi.py <start_date> <end_date>
<start_date> e.g.: 2020-01-01
<end_date> : e.g.:2020-01-02
                
	 """	
	
	args = shlex.split(' '.join(sys.argv[1:]))

	if args[0] == '-h':
        	print help_msg
		sys.exit()
	try:
		start_date = args[0]
		end_date = args[1]
		
    	except Exception as e:
		print("Exception: " + str(e) + "\n")
		print help_msg
		sys.exit()
		
	cdsaapi(start_date, end_date)
    
        
