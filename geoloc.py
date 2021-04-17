# Importing the Libraries
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os, os.path
from collections import namedtuple



# Function to convert GPS coordinated into degree format
def _convert_to_degress(value):
    # Degree
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
    
    # Minute
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
    
    # Second
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
    
    val = d + (m / 60.0) + (s / 3600.0)
    return val

# Function to return the value if the attribute value exist
def _get_if_exist(data,key):
    if key in data:
        return data[key]
    return None

# Function to return the longitude and latitude
def get_lat_lon(exif_data):
    # Defining initial value of latitude and longitude data as None
    lat = None
    lon = None
    
    # If GPSInfo is present in our retrieved exif data then retrieve all other attribute of exif data
    if "GPSInfo" in exif_data:
        # Retrieving through GPSInfo key in exif data
        gps_info = exif_data["GPSInfo"]
        
        # Retrieving the Latitude, Longitude, LatitudeRef and LongitudeRef from our data if it exists
        # If you want to know what all these data are please check the link below:
        # Reference: https://exiftool.org/TagNames/GPS.html
        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
        
        # If we get all the coordinates correctly then converting these GPS data into degree format
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            # If Latitude ref is not North
            if gps_latitude_ref != "N":                     
                lat = 0 - lat
            # If Longitude ref is not East
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
    # Returning Our Final data        
    return lat, lon

# Function to return the exif data in the form of a directory
def get_exif_data(image):
    '''
    EXIF data is stored data in an image file that includes the date the photo was taken, resolution, shutter speed, focal length, and other camera settings. 
    Getting the EXIF data for an image results in a dictionary indexed by EXIF numeric tags.
    '''
    info = image._getexif()
    # If there is no exif data then return None
    if(info is None):
        return info
    exif_data = {}
    # For the different tags and value we got from our exif data 
    # Let's get GPSInfo and other required value which we will use
    for tag, value in info.items():
        # Getting the required data from the dictionary
        decoded = TAGS.get(tag, tag)
        # Pulling out the GPS specific tags
        if(decoded == "GPSInfo"):
            gps_data = {}
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]
                
            exif_data[decoded] = gps_data
        else:
            exif_data[decoded] = value
    return exif_data

# Main Function
if __name__ == "__main__":
    
    
    # retriving all the images from the given images folder
    imageDir = "images/" 
    image_path_list = []
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".tif", ".tiff"] 
    valid_image_extensions = [item.lower() for item in valid_image_extensions]
    
    # Dictionary to store the latitude and longitude value from the photo
    latitude = {}
    longitude = {}
    
    #create a list all files in directory and
    #append files with a vaild extention to image_path_list
    for file in os.listdir(imageDir):
        extension = os.path.splitext(file)[1]
        if extension.lower() not in valid_image_extensions:
            continue
        image_path_list.append(os.path.join(imageDir, file))
    count = 0
    
    # From image path list retriving the image and storing the GPS value in defined dictionary
    for i in range(0, len(image_path_list)):
        img = image_path_list[i]
        # Opening the image
        image = Image.open(img)
        # Retrieving the exif data from the image
        exif_data = get_exif_data(image)
        # If exif data is there then retrieve the latitude and longitude data
        # Process these data and store it in our requried dictionary
        if(exif_data == None):
            count+=1
            continue
        else:
            lat, lon = get_lat_lon(exif_data)
            latitude[i] = lat
            longitude[i] = lon
            
    
