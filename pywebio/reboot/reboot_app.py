from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server
from pywebio_battery import *
import time

def main():
    put_markdown('# Reboot System')
    
    def reboot_callback(btn):
        if btn == 'Reboot':
            put_text('Server is rebooting...')  # Display rebooting message
            for i in range(5, 0, -1):
                put_text(f"Countdown: {i} seconds")
                time.sleep(1)
            put_text('Server is offline. Please wait for reboot...')
    
    put_buttons(['Reboot'], onclick=reboot_callback)
    
if _name_ == '__main__':
    start_server(main, debug=True, port=8080)  # Use port 8080 or another available port

