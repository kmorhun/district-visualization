import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from time import sleep
from datetime import datetime
import csv

def get_master_address_list(csv_file):
    csvfile = open(csv_file, 'r', newline='')

    #for file naming
    now = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')

    reader = csv.DictReader(csvfile)

    #write the header of the output file
    output = open(f"data/addresses{now}.csv", 'w', newline='')
    writer = csv.DictWriter(output, fieldnames=["address", "elementary", "middle", "high_school", "lat", "lon"])
    writer.writeheader()
    output.close()

    temp_list = []
    count = 0
    for row in reader:
        sleep(1) # to follow nominatim terms of service
        street = row["Street "].strip()
        side = row["Side "].strip() #All, Even, or Odd
        low = int(row["Low "])
        high = int(row["High "])
        elementary = row["Elementary "].strip()
        middle = row["Middle "].strip()
        high_school = row["High School"].strip()
        
        if side.strip().lower() == 'all':
            for i in range(low, high+1):
                address = str(i) + " " + street + " Ridgewood, NJ"
                print(f"getting location for {address}...")
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None).raw
                print(location["lon"], location["lat"])
                
                temp_list.append({"address": address, "elementary": elementary, "middle": middle, "high_school": high_school, "lat": location["lat"], "lon": location["lon"]})
                count += 1
                if count % 10 == 0:
                    print(f"geolocated {count} addresses")
                    write_to_csv(f"data/addresses{now}.csv", temp_list)
                    temp_list = []
        elif side.strip().lower() == "even":
            new_low = low if low % 2 == 0 else low + 1
            for i in range(new_low, high+1, 2):
                address = str(i) + " " + street + " Ridgewood, NJ"
                print(f"getting location for {address}...")
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None).raw
                print(location["lon"], location["lat"])
                
                temp_list.append({"address": address, "elementary": elementary, "middle": middle, "high_school": high_school, "lat": location["lat"], "lon": location["lon"]})
                count += 1
                if count % 10 == 0:
                    print(f"geolocated {count} addresses")
                    write_to_csv(f"data/addresses{now}.csv", temp_list)
                    temp_list = []
        elif side.strip().lower() == "odd":
            new_low = low if low % 2 == 1 else low + 1
            for i in range(new_low+1, high+1, 2):
                address = str(i) + " " + street + " Ridgewood, NJ"
                print(f"getting location for {address}...")
                location = Nominatim(user_agent='district-vis').geocode(address, timeout=None).raw
                print(location["lon"], location["lat"])
                
                temp_list.append({"address": address, "elementary": elementary, "middle": middle, "high_school": high_school, "lat": location["lat"], "lon": location["lon"]})
                count += 1
                if count % 10 == 0:
                    print(f"geolocated {count} addresses")
                    write_to_csv(f"data/addresses{now}.csv", temp_list)
                    temp_list = []
        else:
            print(f"Error: Invalid side, side = {side}")
    
    write_to_csv(f"data/addresses{now}.csv", temp_list)
    temp_list = []
    csvfile.close()

def write_to_csv(csv_file, list):
    output = open(csv_file, 'a', newline='')
    writer = csv.DictWriter(output, fieldnames=["address", "elementary", "middle", "high_school", "lat", "lon"])
    for el in list:
        writer.writerow(el)
    output.close()

def add_geometry(gdf):
    #expects the gdf to have "lat" and "lon" columns
    gdf['geometry'] = [Point(xy) for xy in zip(gdf["lon"], gdf["lat"])] 

def save_shape_file(address_csv):
    my_gdf = gpd.read_file(address_csv)

    # this is to just get the file name
    address_file_name = address_csv.split("/")[-1][:-4]
    add_geometry(my_gdf)
    print(my_gdf.head())
    my_gdf.to_file(f'shapefiles/{address_file_name}.shp')  


if __name__ == "__main__":
    # print(get_master_address_list("data/addresses_raw_small.csv"))
    # save_shape_file("data/addresses_2023_12_26_21_42_39.csv")
    save_shape_file("data/addresses_2023_12_26_22_00_49.csv")