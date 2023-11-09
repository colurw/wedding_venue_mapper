# Wedding_Venue_Mapper 

Searches for wedding venues based on name and geographic criteria. Based on the Approved Premises List, 
available at https://www.gov.uk/government/publications/civil-marriages-and-partnerships-approved-premises-list 

## 1_data_cleaning.py 

Converts a spreadsheet into a Pandas dataframe, then cross references the venue's postcode against OS CodePoint 
data to find its latitude and longitiude.  Then calculates of the distance to the nearest station and airport, 
based their coordinates or postcode respectively.

## 2_draw_map.py 

Filters the list of venues according to user criteria, then generates an interactive map in the browser using 
Plotly and Open Street Map.

![image](https://github.com/colurw/wedding_venue_mapper/assets/66322644/d544b381-921c-44dd-8399-4eb0f9eb6023)
