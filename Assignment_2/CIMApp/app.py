from flask import Flask, request, render_template
import pywbem
from subprocess import check_output as out

app = Flask(__name__)

@app.route('/CIM', methods=['POST'])
def cim():
    name = request.form['name']
    wbem = pywbem.WBEMConnection(name)
    os = wbem.EnumerateInstances('CIM_OperatingSystem')[0]['Version'].split()
    os = os[0] + '\n' + os[1]
    interface = ''
    interfaces = wbem.EnumerateInstances('CIM_IPProtocolEndpoint')
    for i in interfaces:
        interface += 'Name=' + i['Name'] + '\nIPv4Address=' + i['IPv4Address'] + '\n\n'
    return render_template('index.html', os=os, interface=interface)

@app.route('/SNMP', methods=['POST'])
def snmp():
    name = request.form['name']
    query = 'snmpwalk -v 2c -c ttm4128 ' + name + ' 1.3.6.1.2.1.1.1'
    try:
        snmp = out(query.split()).split('"')[1]
    except:
        snmp = 'Error: SNMP Service not running on ' + name
    query = 'snmpwalk -v 2c -c ttm4128 ' + name + ' 1.3.6.1.2.1.4.20.1.1'
    try:
        snmp_interface = 'IPv4Address=' + out(query.split()).split()[7]
    except:
        snmp_interface = ''
    return render_template('index.html', snmp=snmp, snmp_interface=snmp_interface)

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
