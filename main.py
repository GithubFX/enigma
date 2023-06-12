import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser

def get_photo_location(file_path):
    try:
        with Image.open(file_path) as image:
            if hasattr(image, '_getexif'):
                exif_data = image._getexif()
                if exif_data is not None:
                    for tag_id, value in exif_data.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        if tag_name == 'GPSInfo':
                            gps_info = {}
                            for key in value.keys():
                                sub_tag_name = GPSTAGS.get(key, key)
                                gps_info[sub_tag_name] = value[key]

                            latitude = gps_info.get('GPSLatitude')
                            longitude = gps_info.get('GPSLongitude')
                            latitude_ref = gps_info.get('GPSLatitudeRef')
                            longitude_ref = gps_info.get('GPSLongitudeRef')

                            if latitude and longitude and latitude_ref and longitude_ref:
                                latitude_decimal = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
                                longitude_decimal = longitude[0] + longitude[1] / 60 + longitude[2] / 3600

                                if latitude_ref == 'S':
                                    latitude_decimal = -latitude_decimal
                                if longitude_ref == 'W':
                                    longitude_decimal = -longitude_decimal

                                decimal_string = str(float(longitude_decimal))
                                print("Longitude:", decimal_string)

                                decimal_string2 = str(float(latitude_decimal))
                                print("Latitude:", decimal_string2)

                                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={decimal_string2},{decimal_string}"
                                webbrowser.open(google_maps_url)
                            else:
                                print("Location data not found.")
                            break
                    else:
                        print("Location data not found.")
                else:
                    print("No metadata found.")
            else:
                print("No metadata found.")
    except OSError as e:
        print(f"Error opening image: {e}")

# Check if the image path is provided as a command-line argument
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    get_photo_location(file_path)
else:
    print("Please provide the image path as a command-line argument.")
