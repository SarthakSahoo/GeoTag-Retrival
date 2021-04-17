# GeoTag-Retrival
This project work specifically focuses on how to retrieve latituge and longitude data that are stored as meta-data in images using Python programming.

 ## Requirements
 PIL (Pillow is the friendly PIL fork. PIL is the Python Imaging Library, adds image processing capabilities to Python interpreter. This package is best used for getting Exif data such as different TAGS and GPSTAGS)
 
The below command can be used to install our required package for work:
``` 
conda install -c anaconda pillow
```
## Algorithm
The Algorithm that has been used for retriving GeoTag data from Image is:
```
1. Define the path of the folder which is containing all the images
2. Create an Empty list to store all our Image Path.
3. Create a list for storing all the valid extensions of images in a list which we will use.
4. Create two dictionary latitude and longitude to store respective data.
5. Iterate over all the files in required folder and store valid file with extension in Image path list.
6. For all the images stored in Image path list open the image and retrieve the exif data.
7. If exif data is None or No exif data:
8.     then continue
9. else:
10.    retrieve latitude and longitude data from exif data and store it in respective dictionary
```
