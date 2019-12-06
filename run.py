import os
import socket
from art import *

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

tprint('english-2-kamayo')
print('To use this API please be sure that you have an internet connection \nthe android device and laptop must connected to same router or wifi \nFollow this instructions.')
print('1. Open your android project in android studio.')
print('2. Navigate to res > values then find strings.xml')
print('3. Find this item <string name="kamayoBaseUrl">http://192.168.1.6:5000/</string>')
print('4. Replace the item into <string name="kamayoBaseUrl">http://'+IP+':5000</string>')
print('5. Please wait until you see * Running on http://'+IP+':5000')
print('\n')
os.system('python translator_web/flaskr.py')



