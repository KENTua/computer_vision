import pyautogui
import pyperclip
import keyboard
from PIL import Image
import pytesseract
import cv2
import numpy
from rich import print
from rich.console import Console
from random import randint, uniform
from time import sleep
from plyer import notification
from peewee import Model, SqliteDatabase, CharField


db = SqliteDatabase('data.db')
class Nicknames(Model):
   nickname = CharField(primary_key=True)
   class Meta:
      database = db
#Nicknames.delete().execute()
#exit()

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def screenshot_players():
    #screenshot window with all players
    left = 30
    top = 263
    width = 370 #ширина
    height = 330 #высота
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save("players/window.png")


def modify_image(pillow_image,image_path):
    cv_image = cv2.cvtColor(numpy.array(pillow_image), cv2.COLOR_RGB2BGR)
    modified_image= cv2.resize(cv_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(image_path, modified_image)
    return modified_image


def crop_players():
    image = Image.open('players/window.png')
    left = 0
    top = 0
    width = 370 #ширина
    height = 19
    for i in range(17):
        player_image = image.crop((left, top, left + width, top + height))
        player_image.save(f'players/player_{str(i)}.png')
        
        nickname_image=player_image.crop((0,0,95,19))
        nickname_image.save(f'players/nickname_{str(i)}.png')
        modified_nickname=modify_image(nickname_image,f'players/nickname_{str(i)}.png')
        nickname= pytesseract.image_to_string(modified_nickname, lang='rus+eng').replace('\n', '').replace('.', '').replace(' ','').replace('—','').replace('©','').replace('=','').replace('<','')
        #print(str(i), nickname)

        race_image=player_image.crop((135,0,255,19))
        race_image.save(f'players/class_{str(i)}.png')
        modified_race=modify_image(race_image,f'players/class_{str(i)}.png')
        race= pytesseract.image_to_string(modified_race, lang='rus').replace('\n', '').replace('.', '')
        #print(str(i), race)

        level_image=player_image.crop((265,0,290,19))
        level_image.save(f'players/level_{str(i)}.png')
        modified_level=modify_image(level_image,f'players/level_{str(i)}.png')
        level= pytesseract.image_to_string(modified_level, config=r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789').replace('\n', '').replace('.', '')
        #print(str(i), level)
        
        class_image=player_image.crop((295,0,370,19))
        class_image.save(f'players/class_{str(i)}.png')
        modified_class=modify_image(class_image,f'players/class_{str(i)}.png')
        class_= pytesseract.image_to_string(modified_class, lang='rus').replace('\n', '').replace('.', '')
        #print(str(i), class_)
        print([i,nickname,race,level,class_])

        top=top+height

        if nickname!='':
            if level=='80':
                invite(nickname)
                
            elif 'Чернокниж' in class_ or 'Ночная' in race or 'Высшая' in race or 'Вульпера'in race or 'Орк'in race or 'Ворген'in race or 'Эльфийка'in race:
                invite(nickname)
                
    '''
    отступ между строками 10 пикселей
    строка 10 пикселей
    17 строк в окне
    '''


def refresh_click():
    #startButton = pyautogui.locateOnScreen('refresh_btn.png', confidence=0.9)
    # y 635-655
    # x 30 - 125
    x=randint(30, 125)
    y=randint(640, 655)
    speed=uniform(0.5, 0.8)
    pyautogui.moveTo(x, y, speed,pyautogui.easeOutQuad) # start fast, end slow
    pyautogui.click()


def invite(nickname):
    sleep(randint(4,9))
    query = Nicknames.select().where(Nicknames.nickname == nickname)
    if len(query)==0:
        Console().print(f'Invited [red]{nickname}[/red]')
        Nicknames.create(nickname=nickname)
        x=randint(515,650)
        y=randint(640, 655)
        speed=uniform(0.5, 0.8)

        pyautogui.moveTo(x, y, speed,pyautogui.easeOutQuad) # start fast, end slow
        pyautogui.click()
        sleep(uniform(0.4,0.8))
        pyperclip.copy(nickname)
        keyboard.press_and_release('ctrl + v')
        sleep(randint(1,2))
        pyautogui.press('enter')  # press the Enter key


sleep(2)

while True:
    refresh_click()
    sleep(1)

    screenshot_players()

    crop_players()
    notification.notify(
                title='Inviter',
                message='script exited',
                app_name='Spred Screener app_name',
            )
    sleep(randint(5*60,7*60))

'''
0,0       X increases -->
+---------------------------+
|                           | Y increases
|                           |     |
|   1920 x 1080 screen      |     |
|                           |     V
|                           |
|                           |
+---------------------------+ 1919, 1079
'''

