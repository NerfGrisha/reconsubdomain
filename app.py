from flask import Flask, render_template, request, jsonify
import subprocess
import socket

app = Flask(__name__)

# Helper function for performing network scans
def perform_scan(url, tool):
    try:
        if tool == "nmap":
            return subprocess.check_output(['nmap', '-F', socket.gethostbyname(url)]).decode('utf-8')
        elif tool == "whois":
            # Specify the WHOIS server for .id domains (Indonesia)
            whois_server = 'whois.idnic.net.id'
            return subprocess.check_output(['whois', '-h', whois_server, url]).decode('utf-8')
        else:
            return "Undefined tool"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.returncode}\n{e.output.decode('utf-8')}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools', methods=['GET', 'POST'])
def tools():
    return render_template('tools.html')

@app.route('/run_nmap', methods=['POST'])
def run_nmap():
    data = request.get_json()
    target = data.get('target')
    result = perform_scan(target, "nmap")
    return result

@app.route('/run_whois', methods=['POST'])
def run_whois():
    data = request.get_json()
    domain = data.get('domain')
    result = perform_scan(domain, "whois")
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
