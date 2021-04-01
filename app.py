#!/usr/bin/python3

from flask import Flask, flash, redirect, render_template, request, session, abort
# from blinkt import set_pixel, set_brightness, show, clear
import colorsys
import logging
import time
import os
import pyotp
import qrcode

KEY_FILENAME = 'gentle_alarm_totp.key'
QR_FILENAME = 'static/qrcode.png'
MFA_NAME = 'GentleAlarm'

Secret = None

logging.basicConfig()
app = Flask(__name__)


def totp_setup_and_get_qrcode():
    secret = pyotp.random_base32()
    with open(KEY_FILENAME, 'w') as keyfile:
        keyfile.write(secret)
    qrcode_url = pyotp.TOTP(secret).provisioning_uri(issuer_name=MFA_NAME)
    qrcode.make(qrcode_url).save(QR_FILENAME)
    
    return qrcode_url
    

@app.route('/')
def home():
    if not session.get('logged_in'):
        context = {
            'initial_setup': False
        }

        if ((not os.path.isfile(KEY_FILENAME)) or (os.path.isfile(QR_FILENAME))):
            logging.info('Keyfile does not exist!  Beginning initial setup.')

            qrcode_url = totp_setup_and_get_qrcode()
            context = {
                'initial_setup': True
                ,'qrcode_filename': QR_FILENAME
                ,'qrcode_url': qrcode_url
            }

        session['wrong_attempts'] = 0 if not session.get('wrong_attempts') else session.get('wrong_attempts')
        return render_template('login.html', **context)
    else:
        return render_template('blinkt.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    with open(KEY_FILENAME, 'r') as keyfile:
        Secret = keyfile.read()

    if request.form['pin'] == pyotp.TOTP(Secret).now():
        if (os.path.isfile(QR_FILENAME)):
            # Initial setup is successful, if a login is performed while the qr code file exists.
            os.remove(QR_FILENAME)

        session['logged_in'] = True
    else:
        session['wrong_attempts'] += 1
    return home()


@app.route('/off')
def off():
    '''
    clear()
    show()
    '''
    return render_template('index.html')


@app.route('/mwl')
def mwl():    
    t = 2
    while t > 0:
        for i in range(8):
            '''
            clear()
            set_pixel(i, 255, 255, 255)
            show()
            '''
            time.sleep(0.05)
        t = t - 1  
    return render_template('index.html')  
        

@app.route('/rainbow')
def rainbow():     
    spacing = 360.0 / 16.0
    hue = 0
    # set_brightness(0.1)
    t = 16
    while t > 0:
        hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            # set_pixel(x, r, g, b)
        # show()
        time.sleep(0.05)
        t = t - 1            
    return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True)