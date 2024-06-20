from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pywebio import start_server
from pywebio_battery import *

def main():
    put_markdown('# Reboot System')
   
    def reboot_callback(btn):
        if btn == 'Reboot':
            user_confirmed = confirm("Are you sure you want to reboot?")
            if user_confirmed:
                run_shell("sudo reboot")
    
    put_buttons(['Reboot'], onclick=reboot_callback)
    
if __name__ == '__main__':
    start_server(main, debug=True, port=18080)


