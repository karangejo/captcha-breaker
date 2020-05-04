# can be somewhat successfull breaking the captcha for this site:
# http://service.etax.nat.gov.tw/etwmain/web/ETW113W1_2

import pytesseract
import sys
import argparse
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output


def resolve(path):
	print("Resampling the Image",path)
	new_path = "new"+path
	# image processing 
	# this might need to be changed depending on what the captcha looks like
	out = check_output(['convert', path, '-resample', '600', new_path])
	out = check_output(['convert', new_path, '-colorspace', 'Gray', new_path])
	out = check_output(['convert', new_path, '-white-threshold', '50%', new_path])
	out = check_output(['convert', new_path, '+dither', '-colors', '2', new_path])
	out = check_output(['convert', new_path, '-white-threshold', '50%', new_path])	
	out = check_output(['convert', new_path, '-shave', '10x10', new_path])
	out = check_output(['convert', new_path, '-blur', '0x8', new_path])
	out = check_output(['convert', new_path, '-sharpen', '0x8', new_path])
	return pytesseract.image_to_string(Image.open(new_path))

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('path',help = 'Captcha file path')
	args = argparser.parse_args()
	path = args.path
	print('Resolving Captcha')
	captcha_text = resolve(path)
	print('Extracted Text',captcha_text)


