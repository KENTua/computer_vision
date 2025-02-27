import pyautogui
import pyperclip
import keyboard
from PIL import Image
import pytesseract
import cv2
import numpy
import cloudscraper
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

BLACKLIST=[
    'Odesza',
    'Aiyu',
    'Саняленин'
]

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

scraper = cloudscraper.create_scraper()
def get_info_from_site(nickname:str)->dict:
    resp= scraper.get(f'https://sirus.su/api/base/42/character/{nickname}?lang=ru')
    try:
        js=resp.json()['character']
    except:
        Console().print(f'Error getting [red]{nickname}[/red] from site')
        return {}
    #guild=js['guildName'] None if without guild
    player_info={'level':js['level'],'race':js['raceName'],'class_':js['className']}
    print(player_info)
    return player_info


def screenshot_players():
    #screenshot window with all players
    left = 30
    top = 263
    width = 370 #ширина
    height = 330 #высота
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save("players/window.png")


def modify_image(pillow_image,image_path,invert=False):
    cv_image = cv2.cvtColor(numpy.array(pillow_image), cv2.COLOR_RGB2BGR)
    modified_image= cv2.resize(cv_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    if invert==True:
        modified_image = cv2.bitwise_not(modified_image)
    #cv2.imwrite(image_path, modified_image)
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
        #nickname_image.save(f'players/nickname_{str(i)}.png')
        modified_nickname=modify_image(nickname_image,f'players/nickname_{str(i)}.png',invert=True)
        nickname= pytesseract.image_to_string(modified_nickname,config='--psm 7', lang='rus+eng').replace('\n', '').replace('.', '').replace(' ','').replace('—','').replace('©','').replace('=','').replace('<','').replace('_','').replace('|','')
        #print(str(i), nickname)
        '''
        ilvl_image=player_image.crop((100,0,125,19))
        ilvl_image.save(f'players/ilvl_{str(i)}.png')
        modified_ilvl=modify_image(ilvl_image,f'players/ilvl_{str(i)}.png',invert=True)
        ilvl= pytesseract.image_to_string(modified_ilvl, config=r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789').replace('\n', '').replace('.', '')
        #print(str(i), ilvl)
        '''
        race_image=player_image.crop((135,0,255,19))
        #race_image.save(f'players/class_{str(i)}.png')
        modified_race=modify_image(race_image,f'players/class_{str(i)}.png')
        race= pytesseract.image_to_string(modified_race, config='--psm 7', lang='rus').replace('\n', '').replace('.', '')
        #print(str(i), race)

        level_image=player_image.crop((265,0,290,19))
        #level_image.save(f'players/level_{str(i)}.png')
        modified_level=modify_image(level_image,f'players/level_{str(i)}.png',invert=True)
        level= pytesseract.image_to_string(modified_level, config=r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789').replace('\n', '').replace('.', '')
        #print(str(i), level)
        
        class_image=player_image.crop((295,0,370,19))
        #class_image.save(f'players/class_{str(i)}.png')
        modified_class=modify_image(class_image,f'players/class_{str(i)}.png')
        class_= pytesseract.image_to_string(modified_class, lang='rus').replace('\n', '').replace('.', '')
        #print(str(i), class_)
        print([i,nickname,race,level,class_])

        top=top+height

        blacklist_levels=['1','2','3','4','5']
        if level in blacklist_levels:
            nickname=''
        
        if nickname!='':
            query = Nicknames.select().where(Nicknames.nickname == nickname)
            if len(query)==0 and nickname not in BLACKLIST:
                if level=='80':
                    invite(nickname)
                else:
                    if class_=='' or level =='' or race=='':
                        player_info=get_info_from_site(nickname)#{'level':js['level'],'race':js['raceName'],'class_':js['className']}
                        if player_info!={}:
                            class_=player_info['class_']
                            race=player_info['race']
                            level=player_info['level']
                    if 'Вульпера'in race: # 'Чернокниж' in class_ or
                        invite(nickname)
                    elif 'Ночная' in race or 'Высшая' in race or 'Орк'in race or 'Эльфийка'in race:
                        level=int(level)
                        if level>60:
                            invite(nickname)
                
                Nicknames.create(nickname=nickname)
            else:
                print(nickname,' in blacklist')
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
    Console().print(f'Invited [yellow]{nickname}[/yellow]')
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


def main():
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
        print('------------------')
        sleep(randint(3*60,5*60))

sleep(2)
main()


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

