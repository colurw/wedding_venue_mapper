Wedding_Venue_Mapper searches for potential wedding venues based on name and geographic criteria.

It's based on the Approved Premises List, which is available (in a horrifically-formatted spreadsheet)
at https://www.gov.uk/government/publications/civil-marriages-and-partnerships-approved-premises-list 

1_data_cleaning.py converts this spreadsheet into a pandas dataframe, and uses the venue's postcode
to get the latitude and longitiude, then calculates the distance to the nearest station and airport.

2_draw_map.py filters the venues according to preference, then generates an interactive map in the
browser using Plotly and Open Street Map.