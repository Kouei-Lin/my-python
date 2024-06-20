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
                put_html('<div id="countdown">Reloading in <span id="countdown-span">60</span> seconds...</div>')
                js_code = """
                <script>
                var seconds = 60;
                var countdown = setInterval(function() {
                    seconds--;
                    document.getElementById('countdown-span').textContent = seconds;
                    if (seconds <= 0) {
                        clearInterval(countdown);
                        // Add a delay before rebooting
                        setTimeout(function() {
                            location.reload();
                        }, 5000); // 5000 milliseconds (5 seconds) delay
                    }
                }, 1000);
                </script>
                """
                put_html(js_code)
                run_shell("sudo reboot")
    
    put_buttons(['Reboot'], onclick=reboot_callback)
    
if _name_ == '__main__':
    start_server(main, debug=True, port=18080)

