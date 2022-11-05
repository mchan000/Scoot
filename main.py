import requests
import gmplot
import googlemaps


if __name__ == '__main__':
    # plot
    gmap = gmplot.GoogleMapPlotter(44.96958573636865, -93.22526591407879, 18, apikey='')


    # Spin available scooters API
    url = 'https://gbfs.spin.pm/api/gbfs/v2/minneapolis/free_bike_status'
    response = requests.get(url)
    spinScoot = response.json()['data']['bikes']
    spinFree = {}
    lats = []
    lons = []
    # Loop through and add lattitudes and longitudes of non-reserved, non-dead scooters
    for i in range(len(spinScoot)):
        if spinScoot[i]['is_reserved'] == False and spinScoot[i]['is_disabled'] == False:
            spinFree[spinScoot[i]['bike_id']] = (spinScoot[i]['lat'], spinScoot[i]['lon'])
            lats.append(spinScoot[i]['lat'])
            lons.append(spinScoot[i]['lon'])
    # Add lats and lons to google maps
    gmap.scatter(lats, lons, size=10, marker=True, color='orange', )

    # Lyft available scotters API
    url = 'https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/msp/free_bike_status.json'
    response = requests.get(url)
    lyftScoot = response.json()
    lyftFree = {}
    lyftLats = []
    lyftLons = []
    for entity in lyftScoot['data']['bikes']:
        if entity['is_reserved'] == 0 and entity['is_disabled'] == 0 \
                and entity['type'] == 'electric_scooter':
            lyftFree[entity['bike_id']] = (entity['lat'], entity['lon'])
            lyftLats.append(entity['lat'])
            lyftLons.append(entity['lon'])

    gmap.scatter(lyftLats, lyftLons, size=10, marker=True, color='purple')

    # Lime available scotters API
    ne_lat = '44.976'
    ne_lng = '-93.21382'
    sw_lat = '44.967'
    sw_lng = '-93.238'
    cookie = '<cookie>'
    header = {'authorization': 'Bearer <bearer>'}
    url = 'https://web-production.lime.bike/api/rider/v1/views/map?ne_lat=' + ne_lat + '&ne_lng=' + ne_lng + '&sw_lat=' + sw_lat + '&sw_lng=' + sw_lng + '&user_latitude=44.9695&user_longitude=-93.2252&zoom=100'
    response = requests.get(url, headers=header)
    limeScoots = response.json()['data']['attributes']['bikes']
    lats = []
    lons = []
    for i in limeScoots:
        lats.append(i['attributes']['latitude'])
        lons.append(i['attributes']['longitude'])
    gmap.scatter(lats, lons, size=10, marker=True, color='green')
    gmap.draw('index.html')
