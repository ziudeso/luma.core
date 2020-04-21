# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

from PIL import Image, ImageDraw


class canvas(object):
    """
    A canvas returns a properly-sized :py:mod:`PIL.ImageDraw` object onto
    which the caller can draw upon. As soon as the with-block completes, the
    resultant image is flushed onto the device.

    By default, any color (other than black) will be `generally` treated as
    white when displayed on monochrome devices. However, this behaviour can be
    changed by adding ``dither=True`` and the image will be converted from RGB
    space into a 1-bit monochrome image where dithering is employed to
    differentiate colors at the expense of resolution.
    If a ``background`` parameter is provided, the canvas is based on the given
    background. This is useful to e.g. write text on a given background image.
    """
    def __init__(self, device, background=None, dither=False):
        self.draw = None
        if background is None:
            self.image = Image.new("RGB" if dither else device.mode, device.size)
        else:
            assert(background.size == device.size)
            self.image = background.copy()
        self.device = device
        self.dither = dither

    def __enter__(self):
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:

            if self.dither:
                self.image = self.image.convert(self.device.mode)

            # do the drawing onto the device
            self.device.display(self.image)

        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions

    def create(self):
        #return self.__enter__()
        print('create', self)
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def flush(self):
        self.device.display(self.image)


    def cleanup_without_display(self):
        # do the drawing onto the device
        self.device.display(self.image)
        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions 

    def cleanup(self, type, value, traceback):
        #return self.__exit__(None, None, None)
        if type is None:

            if self.dither:
                self.image = self.image.convert(self.device.mode)

            # do the drawing onto the device
            self.device.display(self.image)

        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions
