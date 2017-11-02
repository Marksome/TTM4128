#!/bin/src/python
import os, time, smtplib, matplotlib.pyplot as plt
from subprocess import check_output as out
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def gatherData(agents, dataset): #function to gather the data
    for agent in agents: #runs for every agent you set up
        sysName = ('snmpget -v 2c -c ttm4128 ' + agent + ' iso.3.6.1.2.1.1.5.0').split()
        name = out(sysName).split()[-1] #gets the sysName of the agent
        sysPcks = ('snmpget -v 2c -c ttm4128 ' + agent + ' iso.3.6.1.2.1.4.3.0').split()
        pcks = out(sysPcks).split()[-1] #gets the received packages 
                                        #including errors from the agent
        dataset[name].append(pcks) #append number of packets to dictionary in a list

    return dataset


def plot(name, values): #function to plot the data
    fig = plt.figure()
    plt.plot(values) #plots the values given as input
    fig.suptitle(name + ' - ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    plt.xlabel('Time (s)')
    plt.ylabel('Packages')
    filename = name + '.png' #creates filename with .png
    fig.savefig(filename) #stores the file
    return filename


def sendEmail(dataset): #function to email the data
    FROM = 'Group 8 <group8ttm4128@gmail.com>'
    TO = 'TTM4128 <ttm4128@item.ntnu.no>'
    MESSAGE = MIMEMultipart()
    MESSAGE['Subject']  = 'TTM4128 - Group 8'
    MESSAGE['From'] = FROM
    MESSAGE['To'] = TO
    for name in dataset: 
        msg = MIMEText('Name: ' + str(name) + '\nPackages: ' + str(dataset[name]) + '\n') 
        MESSAGE.attach(msg)

    for name in dataset: #gives name and values from dataset as input to plot()
        filename = plot(name.strip('"'), dataset[name]) #returns the filename stored
        with open(filename, 'rb') as f:
            try:
                image = MIMEImage(f.read()) #reads the stored files
                image.add_header('Content-ID', name)
                MESSAGE.attach(image)
            except:
                print 'Error: could not read image file'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('group8ttm4128@gmail.com', 'group8forlyfe') #login
    try: 
        server.sendmail(FROM, TO, MESSAGE.as_string()) #try to send the email
        print 'Successfully sent email'
    except:
        print 'Error: unable to send email'

    server.quit()


def main():
    agents = ['129.241.209.19','129.241.209.30'] #sahara19 and sahara30
    dataset = defaultdict(list) #dictionary with a list as value
    i = 0 #minute counter
    while i < 16: #runs 15 times (15 minutes)
        gatherData(agents, dataset)
        time.sleep(60) #sleep for 60 seconds
        if i%5==0 and i != 0: #plot data and send email every 5 minutes
            sendEmail(dataset) #gives the dataset as input to sendEmail()
            for name in dataset:
                last = dataset[name][-1] #get last captured package number
                dataset[name] = [last] #set dataset to only contain last
        
        i += 1


main()
