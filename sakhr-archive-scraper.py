__author__ = 'mosab'

import os
import urllib
import requests

from lxml import html


def grab_issue_html(issue_id):
    url = 'http://archivebeta.sakhrit.com/newPreview.aspx?ISSUEID={}'.format(issue_id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    else:
        # raise Er
        pass


def extract_images(issue_html):
    tree = html.fromstring(issue_html)
    issue_images = tree.xpath('//div[contains(@class, "slide")]/img/@src')

    for n, i in enumerate(issue_images):
        image_path = i.replace('\\\\', '/').replace('\\', '/')
        issue_images[n] = 'http://archivebeta.sakhrit.com/{}'.format(image_path)
    return issue_images


def download_issue_images(issue_id, issue_images):
    issue_dir = '{}'.format(issue_id)

    if not os.path.exists(issue_dir):
        os.makedirs(issue_dir)

    for image in issue_images:
        file_name = image.split('/')[-1]
        file_full_name = '{}/{}'.format(issue_dir, file_name)
        print 'Downloading file : "{}"'.format(file_full_name)
        urllib.urlretrieve(image, file_full_name)


if __name__ == '__main__':
    start = 1
    end = 20000
    for i in range(start, end):
        content = grab_issue_html(i)
        images = extract_images(content)

        download_issue_images(i, images)
