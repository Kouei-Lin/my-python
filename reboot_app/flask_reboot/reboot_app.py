from flask import Flask, render_template, request, redirect, url_for, flash
import paramiko

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        username = request.form['username']
        password = request.form['password']
        
        # Perform reboot action
        error = reboot_server(ip, username, password)
        
        if error:
            flash(error, 'error')
        else:
            flash(f'Reboot command sent to {ip}', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

def reboot_server(ip, username, password):
    try:
        # SSH Connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username=username, password=password)
        
        # Reboot command (example: Linux)
        stdin, stdout, stderr = ssh_client.exec_command('sudo reboot')
        
        # Check for errors in the command execution
        error = stderr.read().decode()
        if error:
            return error
        
        # Close SSH connection
        ssh_client.close()
        
        print(f"Reboot command sent to {ip}")
        return None
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

