import random
import urllib
from multiprocessing.pool import ThreadPool
from urllib.request import Request

nwid_data_file_path = "map_clsloc.txt"
folder_for_downloads = "C:/downloads/"
limit_of_pictures = 30
threads_number = 20
timeout = 2

# :param nwid_data_file_path string -> tht with contain nwid and class names
# :param folder_for_downloads string -> folder for photos
# :param limit_of_pictures int -> limit of pictures for each call download_list()
# :param threads_number int -> number of threads to download faster
# :param timeout: int -> for HTTP request timeout in seconds

strings = open(nwid_data_file_path, "r")
wnid_dict = {}
for string in strings:
    spt = string.strip("\n").split(" ")
    wnid_dict[spt[2]] = spt[0]


def get_urls(nwid=wnid_dict['rubber_eraser'], out_folder="", timeout=500):
    feed = []
    url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + nwid
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    urls = response.read().decode('utf-8')
    for i in urls.split('\r\n'):
        feed.append((i, out_folder, timeout))
    return (feed)


def downloader(url_path):
    url, out_folder, timeout = url_path
    try:
        # avoid damaged images
        site = urllib.request.urlopen(url)
        meta = site.info()

        if "ImageWidth" in meta:
            if int(meta["ImageWidth"]) > 300:
                # avoid non jpg images
                if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
                    # download

                    request = urllib.request.urlopen(url, timeout=timeout)
                    with open(out_folder + str(random.randint(10000, 10000000)) + ".jpg", 'wb') as f:
                        try:
                            f.write(request.read())
                            return [True, "done", str(url)]

                        except Exception as e:
                            return [False, " Write error" + str(e), str(url)]

                    # local_filename, _ = urlretrieve(url, out_folder + str(random.randint(10000, 10000000)) + ".jpg")
                    # return [True, "done", str(url) + " saved as:" + local_filename.split("/")[-1]]
                else:
                    return [False, "no jpg or jpeg fail", url]
        else:
            return [False, "ImageWidth fail", url]

    except Exception as e:
        return [False, e, url]


def download_list(nwid_name, folder_for_downloads, limit_of_pictures, threads_number, timeout, is_silent):
    urls = (get_urls(nwid=wnid_dict[nwid_name], out_folder=folder_for_downloads, timeout=timeout))

    for item in (ThreadPool(threads_number).imap_unordered(downloader, urls)):
        if item is not None:
            result, reason, url = item
            if is_silent == False:
                print(reason, url)
            if result:
                limit_of_pictures -= 1
            if limit_of_pictures < 1:
                break
        else:
            print("timeout error ----- ", item)


download_list('rubber_eraser', folder_for_downloads, limit_of_pictures, threads_number, timeout, True)
download_list('crane', folder_for_downloads, limit_of_pictures, threads_number, timeout, True)
download_list('dowitcher', folder_for_downloads, limit_of_pictures, threads_number, timeout, True)
download_list('whiptail', folder_for_downloads, limit_of_pictures, threads_number, timeout, True)
