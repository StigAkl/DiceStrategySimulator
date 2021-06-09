from pynput.mouse import Button, Controller
import time
import pyscreenshot as ImageGrab
import pytesseract

mouse = Controller()
    
def start_auto_bet():
    button_pos = (338, 736)
    mouse.position = button_pos
    time.sleep(1)
    mouse.press(Button.left)
    time.sleep(0.2)
    mouse.release(Button.left)

def has_autobet_stopped():
    time.sleep(2)
    # area of screen
    im=ImageGrab.grab(bbox=(450,1450,850,1530))
    #im.show()
    custom_config = r'--oem 3 --psm 6'
    return "Start" in pytesseract.image_to_string(im, config=custom_config)

num_stopped = 0
while True:
    if has_autobet_stopped():
        start_auto_bet()
        print("Bet stopped, starting..")
        num_stopped += 1
        print("Stopped {} times".format(num_stopped))
    time.sleep(1)