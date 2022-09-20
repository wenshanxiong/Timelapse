from enum import auto
import logging
import subprocess
import numpy as np
import configparser
from PIL import Image

logging.basicConfig(
    filename='logs/record.log',
    format='[%(levelname)s] %(asctime)s %(message)s',
    level=logging.INFO
)

def get_std(exposure):
    subprocess.run(
        [
            'fswebcam', 
            '-c', 'fswebcam.conf', 
            '--set', f'Exposure (Absolute)={exposure}', 
            'sample.jpg'
        ]
    )
    image = np.asarray(Image.open('sample.jpg'))
    std = (np.std(np.sum(image, axis=2)))
    return std

def auto_exposure(target_lower=150, target_upper=200, step_size=10):
    MAX_EXPOSURE = 50
    MIN_EXPOSURE = 3
    config = configparser.ConfigParser()
    config.read('auto_exposure.ini')
    exposure = config.getint('DEFAULT', 'exposure')
    std = get_std(exposure)
    while std > target_upper:
        if exposure - step_size < MIN_EXPOSURE:
            break
        exposure -= step_size
        std = get_std(exposure)
    while std < target_lower:
        if exposure + step_size > MAX_EXPOSURE:
            break
        exposure += step_size
        std = get_std(exposure)
    config['DEFAULT']['exposure'] = str(exposure)
    with open('auto_exposure.ini', 'w') as configfile:
        config.write(configfile)
    return exposure

if __name__ == '__main__':
    auto_exposure()