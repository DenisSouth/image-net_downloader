import os
import random
import urllib
from urllib.request import Request, urlretrieve

# open http://image-net.org/explore?wnid=n00523513
# select other class
# copy wnid= from url
#  run

# or open https://gist.github.com/aaronpolhamus/964a4411c0906315deb9f4a3723aac57 ( map_clsloc.txt)


strings = open("map_clsloc.txt", "r")
wnid_dict = {}
for string in strings:
    spt = string.strip("\n").split(" ")
    wnid_dict[spt[2]] = spt[0]


def store_raw_images(nwid=wnid_dict['rubber_eraser'], limit=200, out_folder="image_net_pics"):
    url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + nwid
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    urls = response.read().decode('utf-8')

    if not os.path.exists('out_folder'):
        os.makedirs('out_folder')

    pic_num = 1
    for i in urls.split('\n'):
        try:
            # avoid damaged images
            site = urllib.request.urlopen(i)
            meta = site.info()

            if "ImageWidth" in meta:
                if int (meta["ImageWidth"])> 300:

                    # download
                    urlretrieve(i, "out_folder/" + str(random.randint(10000, 10000000)) + ".jpg")
                    pic_num += 1

        except Exception as e:
            print(str(e))

        if pic_num > limit:
            break


store_raw_images(nwid=wnid_dict['CD_player'])
