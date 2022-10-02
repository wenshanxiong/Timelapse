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

def auto_exposure(target=195, step_size=10):
    MAX_EXPOSURE = 2047
    MIN_EXPOSURE = 3
    config = configparser.ConfigParser()
    config.read('auto_exposure.ini')
    current_hr = str(datetime.datetime.now().hour)
    if not config.has_section(current_hr):
        config[current_hr] = {'exposure': 25}
    exposure = int(config.get(current_hr, 'exposure'))

    best = exposure
    std = get_std(exposure)
    prev_error = float("inf")
    curr_error = abs(target - std)
    while curr_error < prev_error:
        best = exposure
        if std > target:
            if exposure - step_size < MIN_EXPOSURE:
                break
            exposure -= step_size
        else:
            if exposure + step_size > MAX_EXPOSURE:
                break
            exposure += step_size
        std = get_std(exposure)
        prev_error = curr_error
        curr_error = abs(target - std)
        print(f"std: {std}, target: {target}, diff: {curr_error}")

    config[current_hr]['exposure'] = str(best)
    with open('auto_exposure.ini', 'w') as configfile:
        config.write(configfile)
    logging.info(f'Set exposure to {best}, std = {std}')
    return best

if __name__ == '__main__':
    print(get_std(45))