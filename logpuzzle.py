#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse

def find_last(url):
    return re.findall(r"-(....).jpg", url)


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename) as open_file:
        file_list = open_file.readlines() 
        urls = []  
        for string in file_list:
            current_string = string 
            file_pattern = r'/edu.*.jpg'
            file_match = re.search(file_pattern, current_string)
            if file_match:
                if "http://code.google.com"+file_match.group() not in urls:
                    urls.append("http://code.google.com"+file_match.group())
            else:
                pass
            sorted_urls = sorted(urls, key=find_last)
        for url in sorted_urls:
            print(url + '\n')
        return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    os.mkdir(dest_dir) 
    html_image_tags_string = ''
    for i, img_url in enumerate(img_urls):
        print("Retrieving...: ", img_url)
        urllib.request.urlretrieve(
            img_url, filename=dest_dir + '/img'+str(i)+'.jpg')
        html_image_tags_string = html_image_tags_string + \
            '<img src="img' + str(i) + '.jpg">'
    with open(dest_dir + '/index.html', 'w') as f:
        f.write('<html><body>' + html_image_tags_string +
                '</body></html>')
    return


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
