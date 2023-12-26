import geopandas as gpd
from geopy.geocoders import Nominatim
import time
import os
import ssl

def get_master_address_list():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context 
    
    gdf = gpd.read_file("data/addresses_raw.csv")
    # print(gdf.head())
    new_gdf = gpd.GeoDataFrame(columns=["address", "elementary", "middle", "high_school", "geometry"])
    for iter, row in gdf.iterrows():
        street = row["Street"]
        # print(street)
        side = row["Side"] #All, Even, or Odd
        # print(side)
        low = int(row["Low"])
        high = int(row["High"])
        elementary = row["Elementary"]
        middle = row["Middle"]
        high_school = row["High School"]
        if side.strip().lower() == 'all':
            for i in range(low, high+1):
                address = str(i) + " " + street
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None)
                # location = gpd.tools.geocode(address, provider="nominatim", user_agent="my-application")
                new_gdf = new_gdf.append({"address": str(i) + " " + street, "elementary": elementary, "middle": middle, "high_school": high_school, "geometry": location}, ignore_index=True)
        elif side.strip().lower() == "even":
            new_low = low if low % 2 == 0 else low + 1
            for i in range(new_low, high+1, 2):
                address = str(i) + " " + street
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None)
                # location = gpd.tools.geocode(address, provider="nominatim", user_agent="district-vis")
                new_gdf = new_gdf.append({"address": str(i) + " " + street, "elementary": elementary, "middle": middle, "high_school": high_school, "geometry": location}, ignore_index=True)
        elif side.strip().lower() == "odd":
            new_low = low if low % 2 == 1 else low + 1
            for i in range(new_low+1, high+1, 2):
                address = str(i) + " " + street
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None)
                # location = gpd.tools.geocode(address, provider="nominatim", user_agent="district-vis")
                new_gdf = new_gdf.append({"address": str(i) + " " + street, "elementary": elementary, "middle": middle, "high_school": high_school, "geometry": location}, ignore_index=True)
        else:
            print(f"Error: Invalid side, side = {side}")
    time.sleep(1)
    csv = new_gdf.to_csv("data/addresses.csv")
    return new_gdf

if __name__ == "__main__":
    print(get_master_address_list())