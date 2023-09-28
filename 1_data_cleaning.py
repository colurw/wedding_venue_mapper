
""" data: https://www.gov.uk/government/publications/civil-marriages-and-partnerships-approved-premises-list 
          https://osdatahub.os.uk/downloads/open/CodePointOpen  
          https://github.com/ellcom/UK-Train-Station-Locations """


from pandas_ods_reader import read_ods
import pickle
import csv
from convertbng.util import convert_lonlat
from math import radians, cos, sin, acos


def postcode_lat_lon(postcode):
    """ get exact latitude and longitude of a postcode using OS Code-Point data """
    letters = ''
    northing, easting = None, None
    # get first letters of postcode
    for char in str(postcode.upper()):
        if char.isnumeric():
            break
        letters = letters + char         
    try:
        # find correct csv file
        with open(f'data/codepo_gb/CSV/{letters}.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)  
            # lookup OSGB36 coordinates  
            for row in reader:
                if row[0] == f"{postcode.upper()}":
                    northing, easting = row[3], row[2]
    except:
        northing, easting = None, None
    # convert OSGB36 coordinates to latitude and longitude
    lon, lat = [None], [None]
    if northing and easting:
        lon, lat = convert_lonlat([int(easting)],[int(northing)])   
    return *lat, *lon


def distance(lat1, lon1, lat2, lon2):
    """ returns distance between two points in miles using haversine formula"""
    try:
        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1)) 
        lat2 = radians(float(lat2)) 
        lon2 = radians(float(lon2))
        distance = 3963.0 * acos((sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(lon2-lon1))
    except:
        distance = 1000
    return distance


def dist_to_station(postcode):
    """ returns distance from a postcode to nearest train station in miles """
    max_dist = 100
    # get coordinates of target postcode
    lat1, lon1 = postcode_lat_lon(postcode)
    # iterate through coordinates of stations
    with open('data/uk_train_stations.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)  
        for row in reader:
            lat2, lon2 = row[2], row[3]
            # record least distance to target postcode
            dist = distance(lat1, lon1, lat2, lon2)
            if dist < max_dist:
                max_dist = dist
    return int(max_dist)


def dist_to_airport(postcode):
    """ returns distance from a postcode to nearest airport in miles """
    max_dist = 200
    # get coordinates of target postcode
    lat1, lon1 = postcode_lat_lon(postcode)
    # iterate through postcodes of airports
    with open('data/airport_postcodes.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)  
        for row in reader:
            # calculate coordinates of airport
            lat2, lon2 = postcode_lat_lon(row[0])
            # record least distance to target postcode
            dist = distance(lat1, lon1, lat2, lon2)
            if dist < max_dist:
                max_dist = dist
    return int(max_dist)


# read and tidy data
df_venues = read_ods("data/Approved_premises_1-31_JAN_2023.ods", sheet=1)
df_venues.drop(['unnamed.1', 'unnamed.8'], inplace=True, axis=1)
df_venues.columns =['name', 'address', 'phone']
df_venues.drop(index=df_venues.index[:4],inplace=True)
df_venues = df_venues.dropna(subset=['address'])
df_venues = df_venues.reset_index()
df_venues.drop('index', inplace=True, axis=1)

# merge addresses split across two rows
for row in df_venues.index:
    if df_venues.name[row] == None and df_venues.phone[row] == None:
          df_venues.address[row-1] = str(df_venues.address[row-1])+' '+str(df_venues.address[row])
df_venues = df_venues.dropna(subset=['name'])
df_venues = df_venues.reset_index()
          
# split off postcodes from addresses and send to new column
df_venues['postcode'] = df_venues.apply(lambda row: ' '.join(row.address.split()[-2:]), axis = 1)
df_venues['address'] = df_venues.apply(lambda row: ' '.join(row.address.split()[:-2]), axis = 1)
df_venues = df_venues[['name', 'address', 'postcode', 'phone']]

# add venue latitude and longitude
df_venues["latitude"] = df_venues["postcode"].apply(lambda row: postcode_lat_lon(row)[0])
df_venues["longitude"] = df_venues["postcode"].apply(lambda row: postcode_lat_lon(row)[1])

# drop rows with null lat/lon data
df_venues = df_venues.dropna(subset=['latitude'])

# add distances to nearest airport and station
df_venues["station"] = df_venues["postcode"].apply(lambda row: dist_to_station(row))
df_venues["airport"] = df_venues["postcode"].apply(lambda row: dist_to_airport(row))

# remove index digits from name column
df_venues["name"] = df_venues["name"].apply(lambda row: ''.join(filter(lambda char: not char.isdigit(), row)))

# check dataframe
print(df_venues.tail(10))

# save dataframe
with open('pickled/df_venues.pkl', 'wb') as file:
    pickle.dump(df_venues, file)

