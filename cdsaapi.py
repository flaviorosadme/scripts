import cdsapi
import datetime

in_start_date=raw_input('Insert Start Date in the format yyyy-mm-dd:\n')

in_end_date=raw_input('Insert End Date in the format yyyy-mm-dd:\n')

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
	
