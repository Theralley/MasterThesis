from PIL import Image
from PIL.ExifTags import TAGS

imagename = "Geo/4.jpg"
image = Image.open(imagename)

degree_sign = u"\N{DEGREE SIGN}"
q = 0

# extract EXIF data
exifdata = image.getexif()

# iterating over all EXIF data fields
for tag_id in exifdata:

    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)

    # Use the tag of the pic
    if(tag_id == 34853):
        print('\nPicName: ', imagename)

        a1 = data[2][0][0]
        b1 = data[2][1][0]
        c1 = (data[2][2][0]/data[2][2][1])

        a2 = data[4][0][0]
        b2 = data[4][1][0]
        c2 = (data[4][2][0]/data[2][2][1])

        H = (data[6][0]/data[6][1])

        # Convert Degrees Minutes Seconds to Decimal Degrees
        dd1 = a1 + (b1/60) + (c1/3600)
        dd2 = a2 + (b2/60) + (c2/3600)

        print('Coordinates: ', dd1, dd2)
        print('Height:', H)
