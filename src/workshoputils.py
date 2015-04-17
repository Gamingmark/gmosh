#!/usr/bin/env python3
"""Utilities related to interacting with the steam workshop"""

import gmafile
import re
import http.client
import lzma
import json
import os
from wgety.wgety import Wgety

def workshopinfo(addons):
    url = "http://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1"
    connection = http.client.HTTPConnection("api.steampowered.com")
    addonStr = []

    for i in range(len(addons)):
        addonStr.insert(i, "publishedfileids[%i]=%s" % (i, addons[i]))

    connection.request("POST", url,
        body = "itemcount=%i&%s" % (len(addons), '&'.join(addonStr)),
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        )

    response = connection.getresponse()

    if response.status < 200 or response.status > 300:
        print("Error getting addon info! %s" % response.reason)
        return

    return json.loads(response.read().decode("utf-8"))['response']['publishedfiledetails']


def download(addons, extr):
    info = workshopinfo(addons)
    for res in info:
        if not "title" in res:
            print("Addon does not exist!")
            return

        name = res['title']
        download = res['file_url']

        print("Downloading '%s' from the workshop" % name)

        w = Wgety()
        lzmafile = "%s.gma.lzma" % res['publishedfileid']
        outfile = "%s.gma" % res['publishedfileid']
        w.execute(url = download, filename = lzmafile)

        print("Downloaded '%s' from the workshop. Decompressing..." % name)
        with lzma.open(lzmafile) as lzmaF:
            with open(outfile, "wb") as gma:
                gma.write(lzmaF.read())

        os.remove(lzmafile)

        if not extr: return

        name = re.sub('[\\/:"*?<>|]+', '_', name)
        gmafile.extract(outfile, name)
