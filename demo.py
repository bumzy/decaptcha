#!/usr/bin/env python3
from decaptcha import DeCaptcha
from utils import get_captcha_image
import logging

FORMAT = '[%(levelname)s] %(pathname)s:%(lineno)s %(message)s'
logging.basicConfig(format=FORMAT, level=40)

image_text_list = []
captcha_file = open('./captcha/captcha_text')
for i in range(100):
    captcha_text = captcha_file.readline()
    captcha_text = captcha_text.strip()
    captcha_path = './captcha/%d.png' % i
    image_text_list.append([captcha_path, captcha_text])
captcha_file.close()
# print(image_text_list)

login_url = 'http://bt.byr.cn/login.php'
captcha_image = get_captcha_image(login_url)
decaptcha = DeCaptcha()
decaptcha.train(image_text_list)
decaptcha.dump_model('./captcha_classifier.pkl')
captcha_text = decaptcha.decode(captcha_image)
print('captcha_text: %s' % captcha_text)


decaptcha_copy = DeCaptcha()
decaptcha_copy.load_model('./captcha_classifier.pkl')
captcha_text = decaptcha.decode(captcha_image)
print('captcha_text: %s' % captcha_text)
captcha_image.show()
