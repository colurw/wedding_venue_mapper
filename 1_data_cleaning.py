
""" data: https://www.gov.uk/government/publications/civil-marriages-and-partnerships-approved-premises-list """
"""       https://osdatahub.os.uk/downloads/open/CodePointOpen  """


from pandas_ods_reader import read_ods
import pickle
import csv
from convertbng.util import convert_lonlat


def postcode_lat_lon(postcode):
    """ get exact latitude and lontitude of a postcode using OS Code-Point data """
    letters = ''
    northing, easting = None, None
    # get first letters of postcode
    for char in str(postcode.upper()):
        if char.isnumeric():
            break
        letters = letters + char         
    try:
        # find correct csv file
        with open(f'codepo_gb/CSV/{letters}.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)  
            # lookup OSGB36 coordinates  
            for row in reader:
                if row[0] == f"{postcode.upper()}":
                    northing, easting = row[3], row[2]
    except:
        northing, easting = None, None
    # convert OSGB36 coordinates to latitude and lontitude
    lon, lat = [None], [None]
    if northing and easting:
        lon, lat = convert_lonlat([int(easting)],[int(northing)])    
    return *lat, *lon


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

# add latitude and lontitude columns using Code-Point data
df_venues["latitude"] = df_venues["postcode"].apply(lambda row: postcode_lat_lon(row)[0])
df_venues["longitude"] = df_venues["postcode"].apply(lambda row: postcode_lat_lon(row)[1])

# remove index digits from name column
df_venues["name"] = df_venues["name"].apply(lambda row: ''.join(filter(lambda char: not char.isdigit(), row)))

# check dataframe
print(df_venues.head(10))
print(df_venues.tail(10))

# save dataframe
with open('pickled/df_venues.pkl', 'wb') as file:
    pickle.dump(df_venues, file)

