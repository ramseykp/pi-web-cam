from picamera import PiCamera, Color
import os
import sys
import logging
from time import sleep
#from suncalc import get_position, get_times
import suncalc
from datetime import timezone
import datetime as dt

web_cam_home = '/var/www/html/web-cam/'
images_dst_home = '/media/usb-drive/images/'
log_path = os.path.join(web_cam_home, 'pi_cam_log.log')
web_cam_images = os.path.join(web_cam_home, 'images')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(message)s')
logging.debug("log path located at here " + log_path)

def get_wifi_sun_angle():
    logging.debug('get_wifi_sun_angle function')
    #logging.debug(os.popen('curl ipinfo.io/loc'))
    #lat,lon = os.popen('curl ipinfo.io/loc').read().split(',')
    lat = '45.7'
    lon = '-121.6'
    logging.debug('lat = ' + lat)
    logging.debug('lon = ' + lon)
    date = dt.datetime.now(timezone.utc)
    logging.debug(date)
    sun_position = suncalc.get_position(date, float(lon.strip()), float(lat.strip()))
    alt_radians = sun_position['altitude']
    logging.debug(alt_radians)
    alt_deg = alt_radians * 180 / 3.14159
    logging.debug(alt_deg) 
    logging.debug(sun_position)
    return alt_deg

def move_image(src_img, images_home):
    year = dt.datetime.now().strftime('%Y')
    month = dt.datetime.now().strftime('%m')
    day = dt.datetime.now().strftime('%d')
    image_name = 'image_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
    dst_path = os.path.join(images_home, year, month, day)
    logging.debug(dst_path)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    dst_img = os.path.join(dst_path, image_name)
    logging.debug(dst_img)
    os.popen('cp ' + src_img + " " + dst_img)

def Run_Camera():
    logging.debug("entering Run_Camera() function")
    camera = PiCamera()

    camera.resolution = (3280, 2464)
    #camera.brightness = 60
    #camera.contrast = 60
    camera.framerate = 15
    #camera.rotation = 180

    #camera_sleep_time = 60
    camera_warm_up_time = 3
    src_img = os.path.join(web_cam_images, 'recent_image.jpg')
    logging.debug("src_img = " + src_img)
               

    #while True:
    wifi_sun_angle = get_wifi_sun_angle()
    logging.debug('sun angle = ' + str(wifi_sun_angle))
    if wifi_sun_angle > -5:
        logging.debug('starting camera preview')
        camera.start_preview()
        
        sleep(camera_warm_up_time)
        logging.debug('annotating background')
        camera.annotate_background = Color('black')
        logging.debug('annotating foreground')
        camera.annotate_foreground = Color('white')
        
        logging.debug('capturing date and time')
        formatted_date = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        logging.debug(formatted_date)
        
        logging.debug('annotating text')
        camera.annotate_text = formatted_date
        
        logging.debug('capturing src_img = ' + src_img)
        camera.capture(src_img)
        camera.stop_preview()
        #dst_img = os.path.join(web_cam_images, 'image-' + formatted_date + '.jpg')
        #os.popen('cp ' + src_img + " " + dst_img)
        logging.debug('moving image starting')
        move_image(src_img, images_dst_home)
        logging.debug('moving image finished')
        #sleep(camera_sleep_time)
        #logging.debug("sleep finished - starting camera preview soon..")

try:
    Run_Camera()

except Exception as e:
    logging.error("Exception Rasied--------------------------")
    logging.error(e) 