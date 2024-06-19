from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pywebio import start_server
from pywebio_battery import *

def main():
    put_markdown('# Reboot System')
   
    def reboot_callback(btn):
        run_js('window.location.reload()')
        if btn == 'Reboot':
            run_shell("sudo reboot")
    
    put_buttons(['Reboot'], onclick=reboot_callback)
    
if _name_ == '__main__':
    start_server(main, debug=True, port=8080)  # Use port 8080 or another available port

