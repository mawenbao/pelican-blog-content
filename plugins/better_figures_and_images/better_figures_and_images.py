"""
Better Figures & Images
------------------------

This plugin:

- Adds a style="width: ???px; height: auto;" to each image in the content
- Also adds the width of the contained image to any parent div.figures.
    - If RESPONSIVE_IMAGES == True, also adds style="max-width: 100%;"
- Corrects alt text: if alt == image filename, set alt = ''

TODO: Need to add a test.py for this plugin.

"""

from os import path, access, R_OK

from pelican import signals

from bs4 import BeautifulSoup
from PIL import Image

import logging
logger = logging.getLogger(__name__)

def parse_images(instance):
    if instance._content is None or not 'img' in instance._content:
        return

    content = instance._content[:]
    soup = BeautifulSoup(content)

    for img in soup('img'):
        logger.debug('Better Fig. PATH: %s', instance.settings['PATH'])
        logger.debug('Better Fig. img.src: %s', img['src'])

        img_path, img_filename = path.split(img['src'])

        logger.debug('Better Fig. img_path: %s', img_path)
        logger.debug('Better Fig. img_fname: %s', img_filename)

        if not img_path.startswith('/static'):
            logger.debug('Better Fig. img_path %s not started with /static', img_path)
            continue
        # Build the source image filename
        imgSrc = instance.settings['PATH'] + img_path + '/' + img_filename
        logger.debug('Better Fig. src: %s', imgSrc)
        if not (path.isfile(imgSrc) and access(imgSrc, R_OK)):
            logger.error('Better Fig. Error: image not found: {}'.format(imgSrc))
            continue

        # Open the source image and query dimensions; build style string
        im = Image.open(imgSrc)
        imgWidth = im.size[0]
        imgHeight = im.size[1]

        if img.get('alt') and img['alt'] == img['src']:
            img['alt'] = ''

        if not img.get('width'):
            img['width'] = str(imgWidth) + 'px'

        # for lazyload.js
        if 'NIUX2_LAZY_LOAD' in instance.settings and instance.settings['NIUX2_LAZY_LOAD']:
            if img.get('class'):
                img['class'] += 'lazy'
            else:
                img['class'] = 'lazy'
            img['data-original'] = img['src']
            del img['src']
            img['data-width'] = str(imgWidth) + 'px'
            img['data-height'] = str(imgHeight) + 'px'

    instance._content = soup.decode()

def register():
    signals.content_object_init.connect(parse_images)

