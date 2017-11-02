from flask import Flask, render_template
import pywbem
from subprocess import check_output as out

app = Flask(__name__)
wbem = pywbem.WBEMConnection('http://ttm4128.item.ntnu.no:5988/cimom')

@app.route('/CIM')
def cim():
    os = wbem.EnumerateInstances('CIM_OperatingSystem')[0]['Version']
    interface = ''
    interfaces = wbem.EnumerateInstances('CIM_IPProtocolEndpoint')
    for i in interfaces:
        interface += 'Name=' + i['Name'] + '\nIPv4Address=' + i['IPv4Address'] + '\nSubnetMask=' + i['SubnetMask'] + '\n\n'
    return render_template('index.html', os=os, interface=interface)

@app.route('/SNMP')
def snmp():
    snmp = out('snmpwalk -v 2c -c ttm4128 129.241.200.173 1.3.6.1.2.1.1.1'.split())
    return render_template('index.html', snmp=snmp)

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
