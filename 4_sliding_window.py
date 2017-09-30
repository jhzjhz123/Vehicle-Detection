# -*- coding: utf-8 -*-

import cv2


class ImgScanner(object):
    
    def __init__(self, image, step_y=10, step_x=10, win_y=30, win_x=30):
        self._layer = image
        self._step_x = step_x
        self._step_y = step_y
        self._win_x = win_x
        self._win_y = win_y
        
    def generate_next(self):
        """Generate next patch
        
        # Yields
            y : 
            x
            patch : ndarray, shape of (self._win_y, self._win_x) or (self._win_y, self._win_x, 3)
        """
        
        for y in range(0, self._layer.shape[0] - self._win_y, self._step_y):
            for x in range(0, self._layer.shape[1] - self._win_x, self._step_x):
                yield (y, x, self._layer[y:y + self._win_y, x:x + self._win_x])

    def get_patches(self):
        patches = [window for _, _, window in image_scanner.generate_next()]
        return patches

    def show_process(self):
        for y, x, _ in self.generate_next():
            clone = self._layer.copy()
            cv2.rectangle(clone, (x, y), (x + self._win_x, y + self._win_y), (0, 255, 0), 2)
            cv2.imshow("Test Image Scanner", clone)
            cv2.waitKey(1)
            time.sleep(0.025)


class ImgPyramid(object):
     
    def __init__(self, image, scale=0.7, min_y=30, min_x=30):
        self._layer = image.copy()
        self._scale_for_original = 1.0
        
        self._scale = scale
        self._min_y = min_y
        self._min_x = min_x
     
    def generate_next(self):
        yield self._layer, self._scale_for_original
 
        while True:
            h = int(self._layer.shape[0] * self._scale)
            w = int(self._layer.shape[1] * self._scale)
             
            self._layer = cv2.resize(self._layer, (w, h))
             
            if h < self._min_y or w < self._min_x:
                break
            self._scale_for_original = self._scale_for_original * self._scale
            yield self._layer, self._scale_for_original


if __name__ == "__main__":
    import time
    
    image = cv2.imread("test_images//test1.jpg")[200:400, 200:400, :]
    image_pyramid = ImgPyramid(image)
    
    for layer, _ in image_pyramid.generate_next():
        image_scanner = ImgScanner(layer)
        image_scanner.show_process()
    
    
    
    