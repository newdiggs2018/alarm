import RPi.GPIO as GPIO
import time
import smtplib
import cred

try:
    need_clean = False
    MSG  = '\nLocal Police number is 6363275105. Alarm at home was '
    ALARM_MSG = {True:'triggered', False:'deactivated'}
    print('Setting up SMS...')    
    def send_msg(triggered):
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login( cred.FROM, cred.PASS )
        str_print =''.join([MSG, ALARM_MSG[triggered], ' at ',
                            time.strftime('%I:%M:%S %p')])
        print(str_print)
        server.sendmail(cred.FROM, cred.TO, str_print)
        server.quit()
   
    print('Setting up hardware...')
    PIN = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    next_state = True
    need_clean = True    
    print('Ready!')    
    while True:
        if GPIO.input(PIN) == next_state:
            send_msg(next_state)
            next_state = not next_state
        time.sleep(0.3)
        
except KeyboardInterrupt:
    GPIO.cleanup() 
    need_clean = False

if need_clean:    
    GPIO.cleanup() 
print('\nEnd!')
