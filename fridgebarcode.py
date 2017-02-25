# Dewan Pieterse
# Barcode scanning fridge
# February 2017

import json
import urllib.request
import time
import csv
import datetime
import requests
import datetime

# Test barcodes
# 3046920028363 Lindt Excellence 85% Cacao
# 6009612470083 Sparkling Water
# 4000539032509 Lindt Truffel
# 3046920028721 Lindt Excellence 99% Cacao
# 6003191113171 SinuMax Allergy Sinus 20 Capsules
# 6004201004243 Doom Fogger 350ml


def getItemName(barcode): #Get the name from the interwebs: set in stone
    
    if barcode == "":
        return "Nothing scanned, you idiot."
    
    else:

        url = "http://api.upcdatabase.org/json/c2f655f265833968fa24501a34cd70d1/"  

        requesturl = url + str(barcode) + "/"

        #print(requesturl)

        product = urllib.request.urlopen(requesturl)

        data = json.loads(product.read().decode(product.info().get_param('charset') or 'utf-8'))

        if data['valid'] == 'false':
            return data['reason']
        
        else:
            if data['itemname'] == '':
                return data['description']
            else:
                return (data['itemname'])
            
            
def sendToUPCDB(barcode,name):
    
    url = 'http://api.upcdatabase.org/submit/curl.php'
    
    payload = {'upc': barcode , 'mrsp': '' , 'apikey': 'c2f655f265833968fa24501a34cd70d1' , 'title': name , 'alias': '' , 'description': '' , 'unit': ''}
    
    session = requests.Session()
    r = session.post(url,data=payload) 
    
def daysDifference(date):
    
    import datetime
    
    fmt = ("%Y/%m/%d")
    now = datetime.datetime.now()
    then = datetime.datetime.strptime(date, fmt)
    difference = (now - then).days
    return difference

def writeCSV(fileName,itemList): #Write to the old CSV
    
    outFile = open(fileName,'w')
    writer = csv.writer(outFile, dialect='excel')
    for item in itemList:
        #for i in item:
        writer.writerow(item)
        
    outFile.close()

def writeEmail(itemList):
    
    outFile = open('FridgeContentMail.txt','w')
    counter = 0
    for i in itemList:
        for j in i:
            if counter == 1:
                istring = str(j)#[2:-2]
                outFile.write('{:^8}'.format(istring))
                counter += 1
                
            elif  counter == 2:
                istring = str(j)#[2:-2]
                outFile.write('{:27.31}'.format(istring))
                counter += 1
            
            elif  counter == 3:
                #istring = str(j)#[2:-2]
                #outFile.write('{:>18}'.format(istring))
                counter += 1  
                
            else:
                istring = str(j)#[2:-2]
                outFile.write('{:11}'.format(istring))
                counter += 1                
                                                                                                
        counter = 0
        outFile.write('\n')  
    outFile.close()

def readCSV(fileName): #Used to read the CSV
    
    try:
        inFile = open(fileName, 'r')
        reader = inFile.read()
        fridgeContentList = []
        lineList = reader.split('\n')
        for item in lineList:
            j = item.split(',')
            if len(j) == 1:
                continue
            elif j == ['Date','Count','Name','Barcode']:
                continue
            else:
                fridgeContentList.append(j)
        
        inFile.close()
        return fridgeContentList
    
    except:
        fridgeContentList = []
        return fridgeContentList

#def sendMail(): #Needs work. Not in main(). Functions but not in main. Sends to Dewan and Mia
    
    #import os
    #import smtplib
    #from email import encoders
    #from email.mime.base import MIMEBase
    #from email.mime.multipart import MIMEMultipart
    
    #COMMASPACE = ', '
    
    
    #sender = 'pietersedewan@gmail.com'
    #gmail_password = ''
    #recipients = ['dewanfly@gmail.com']
    
    ## Create the enclosing (outer) message
    #outer = MIMEMultipart()
    #outer['Subject'] = 'Test'
    #outer['To'] = COMMASPACE.join(recipients)
    #outer['From'] = sender
    #outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    ## List of attachments
    #attachments = ['/Users/DewanPieterse/Documents/Barcode Scanner/FridgeContentMail.txt']

    ## Add the attachments to the message
    #for file in attachments:
        #try:
            #with open(file, 'r') as fp:
                #msg = MIMEBase('application', "octet-stream")
                #msg.set_payload(fp.read())
            #encoders.encode_base64(msg)
            #msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            #outer.attach(msg)
        #except:
            #print("Unable to open one of the attachments. Error: ")
            #raise

    #composed = outer.as_string()

    ## Send the email
    #try:
        #with smtplib.SMTP('smtp.gmail.com', 587) as s:
            #s.ehlo()
            #s.starttls()
            #s.ehlo()
            #s.login(sender, gmail_password)
            #s.sendmail(sender, recipients, composed)
            #s.close()
        #print("Email sent!")
    #except:
        #print("Unable to send the email. Error: ")
        #raise

def main(): #Runs main program
    
    fridgeContentList = readCSV('FridgeContent.csv')
    
    barcode = (input("Scan barcode:\n"))
    
    while barcode !="":
        
        name = getItemName(barcode)
        if name == 'Code not found in database.':
            name = input('Enter the name of the product:\n')
            sendToUPCDB(barcode,name)
        
        #if any(name in i for i in fridgeContentList): #name in fridgeContentList: 
            
            #fst,snd = 0,0
            #for k in fridgeContentList:
                #for h in k:
                    #if h == name:
                        
           
           
            #if (fridgeContentList[fridgeContentList.index(name)][0] == time.strftime("%Y/%m/%d")):
                #str(int(fridgeContentList[fridgeContentList.index(name)][2]) + 1)
                
            #else:
                #if (daysDifference(fridgeContentList[fridgeContentList.index(name)][0]) > 7):
                    #fridgeContentList[fridgeContentList.index(name)][0] == time.strftime("%Y/%m/%d")
                    #str(int(fridgeContentList[fridgeContentList.index(name)][2]) + 1)
                    
        #else:
        fridgeContentList.append([time.strftime("%Y/%m/%d"),"1" , name , barcode])
            
        #fridgeContentList.sort()
            
        barcode = input("Scan barcode:\n")
        
    fridgeContentList.insert(0, ['Date','Count','Name','Barcode'])
    
    writeCSV('FridgeContent.csv', fridgeContentList)
    writeEmail(fridgeContentList)
    print('Good bye.')


#main()
#sendMail()
