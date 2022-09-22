from enum import auto
import logging
import subprocess
import numpy as np
import configparser
import datetime
from PIL import Image

logging.basicConfig(
    filename='logs/util.log',
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

def auto_exposure(target_lower=150, target_upper=190, step_size=5):
    MAX_EXPOSURE = 50
    MIN_EXPOSURE = 3
    config = configparser.ConfigParser()
    config.read('auto_exposure.ini')
    current_hr = str(datetime.datetime.now().hour)
    if not config.has_section(current_hr):
        config[current_hr] = {'exposure': 25}
    exposure = int(config.get(current_hr, 'exposure'))
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
    config[current_hr]['exposure'] = str(exposure)
    with open('auto_exposure.ini', 'w') as configfile:
        config.write(configfile)
    logging.info(f'Set exposure to {exposure}, std = {std}')
    return exposure

if __name__ == '__main__':
    print(get_std(45))