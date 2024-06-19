from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server

import subprocess

def execute_command(cmd):
    put_text("Executing command...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            put_code(result.stdout, language='shell')
        else:
            put_text(f"Command execution failed with error:\n{result.stderr}")
    except Exception as e:
        put_text(f"Error occurred during command execution: {str(e)}")

def main():
    put_markdown("# Reboot System")
    put_markdown("Click the button below to reboot the system.")
    put_buttons(['Reboot'], onclick=lambda _: execute_command('reboot'))

if __name__ == '__main__':
    start_server(main, port=8080)

