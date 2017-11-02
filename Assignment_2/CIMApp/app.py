from flask import Flask, render_template
import pywbem, pysnmp

app = Flask(__name__)
conn = pywbem.WBEMConnection('http://ttm4128.item.ntnu.no:5988/cimom')

@app.route('/OS')
def os():
    os = conn.EnumerateInstances('CIM_OperatingSystem')[0]['Version']#.replace(' ', '\n')
    return render_template('index.html', os=os)

@app.route('/CIM')
def cim():
    cim = ''
    interfaces = conn.EnumerateInstances('CIM_IPProtocolEndpoint')
    for i in interfaces:
        cim += 'Name=' + i['Name'] + '\nIPv4Address=' + i['IPv4Address'] + '\nSubnetMask=' + i['SubnetMask'] + '\n\n'
    return render_template('index.html', cim=cim)

@app.route('/SNMP')
def snmp():

    return render_template('index.html', snmp=snmp)

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
