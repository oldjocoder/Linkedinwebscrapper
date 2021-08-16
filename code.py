
import os, time
#import prettify
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re
import requests
import csv
import time
import pandas as pd

print ('please type or paste the navigator search URL' )


salesUrl = input()
userAgent = 'Mozilla/5.0'
profile = webdriver.FirefoxProfile()

print('how many pages you want to extract')
p = input()

print('type your linkedin username')
mail = input()
print('type your Linkedin password')
password = input()

profile.set_preference("general.useragent.override", "Cincobot") #setting the user agent as cincobot 

browser = webdriver.Firefox(profile)  #opens firefox
browser.get(salesUrl)  # takes to linkedin loginn page

frame = browser.find_element_by_tag_name('iframe')#defining the frame for switching 
print(frame)
browser.switch_to_frame(frame) 




email_element = browser.find_element_by_id("username")  #takes to enters username
email_element.send_keys(mail)  # usermane is assigned
pass_element = browser.find_element_by_id("password")  ## takes to enter password
pass_element.send_keys(password)  #password is assigned
pass_element.submit()  #submited
browser.switch_to.default_content()
print("success! Logged in, Bot starting")  # hopeful message
browser.maximize_window()#maximizes browser
#have  to start the loop here 
employeestest = []
for x in range(0, int(p)):

    time.sleep(3) # without this waiting time BS doesn't switch to the the default contant
   
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")#scroll down to the bottom might be redundent
    total_height = int(browser.execute_script("return document.body.scrollHeight"))

    for i in range(1, total_height, 2):
        browser.execute_script("window.scrollTo(0, {});".format(i))
    #print(browser.execute_script("return navigator.userAgent"))
    #print(browser.page_source)
    time.sleep(4) 
    page = bs(browser.page_source,"html.parser")#capturing the html content
    #print(browser)
    #print (page.prettify())
    #print (page)
    #content stores all the href object with regular expression under tag <a>
    content = page.find_all('a',{'href':re.compile(r'/sales/people/\S')})
    #print(content)

    #storing the href element for going to each profile page 
    for items in content:
        employeestest.append(items.get('href'))# this need section to be passed to after https://www.linkedin.com for going to each profile

    #have to go to thge next page 

    python_button = browser.find_elements_by_xpath("/html/body/main/div[1]/div/section/div[2]/nav/button[2]/span")[0]
    python_button.click()
    print('check')


#removing duplicate entries    
employees = [] 
for i in employeestest: 
    if i not in employees: 
       employees.append(i) 

print(len(employees))

# below code is to go to each profile page of all contacts and save name ,designation , emailid , phone , current organization and location
employeeContact = [] # for storing contact information
nameList = []
designationList = []
emailList = []
phoneList = []
companyList = []
locationList = []

for i in employees:
    contactUrl='https://www.linkedin.com' + i
    browser.get(contactUrl)#opening the contect info page
    time.sleep(8) #wait for loading 
    contact_page = bs(browser.page_source, features="html.parser")#capturing content of the page profile page 
        
    #capturing the name 
    name = contact_page.find_all('span', {'class':"profile-topcard-person-entity__name Sans-24px-black-90%-bold"})
    for i in name:
        name1 =i.getText() #converting and taking string object
        employeeContact.append(name1) #storing the name in list 
        nameList.append(name1)
        # print(name1)
        

    #captuing designation 
    designation = contact_page.find_all('span', {'class':"profile-topcard__summary-position-title"})
    designation1 = designation[0].getText()
    employeeContact.append(designation1)
    designationList.append(designation1)
    #print(designation1)

    #capturing email-id
    email = contact_page.find_all('a',href=re.compile("mailto"))
    #print(email)
    if email == []:
        email1 = 'not available'
    else:
        for k in email:
            email1=k.getText()
    #print(email1)
    employeeContact.append(email1)
    emailList.append(email1)

    #email1 = email[0].getText()#need to handle error IndexError: list index out of range
        
    #capturing phone number 
    phone = contact_page.find_all('a',href=re.compile('tel'))
    #print (phone)

    if phone == []:
        phone1 = 'not available' 
    else:
        for l in phone:
            phone1 = l.getText()
    
    employeeContact.append(phone1)
    phoneList.append(phone1)
    #phone1 = phone[0].getText()#need to handle error IndexError: list index out of range
    
    #capturing current company name 
        
    # company = contact_page.find_all('a',{'class':"inverse-link-on-a-light-background font-weight-400 ember-view"})
    company = contact_page.find_all('a',{'class':"li-i18n-linkto inverse-link-on-a-light-background Sans-14px-black-75%-bold"})
    if company == []:
        company1 = 'could not retrive'
    
    else:
        for m in company: 
            company1 = m.getText()
            break
    employeeContact.append(company1)
    companyList.append(company1)
    
    #print(company1)
    #company1 = company[0].getText()# need to handle error IndexError: list index out of range
        
        
    #capturing the location 
    location = contact_page.find_all('div', {'class':"profile-topcard__location-data inline Sans-14px-black-60% mr5"})#works
    for n in location:
        location1 = n.getText()
        employeeContact.append(location1)
        locationList.append(location1)
        
#print(employeeContact) #list with all the contact information 

#removing the new line character
nameList1 = []
for element in nameList:
    str(element).replace(' ','')
    nameList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))
designationList1 = []
for element in designationList:
    str(element).replace(' ','')
    designationList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))
emailList1 = []
for element in emailList:
    str(element).replace(' ','')
    emailList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))
phoneList1 = []
for element in phoneList:
    str(element).replace(' ','')
    phoneList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))
companyList1 = []
for element in companyList:
    str(element).replace(' ','')
    companyList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))
locationList1 = []
for element in locationList:
    str(element).replace(' ','')
    locationList1.append(re.sub(' +', ' ', element.strip().replace("\n","")))

#employeeContact1 = []
for element in employeeContact:
    str(element).replace(' ','')
    #employeeContact1.append(re.sub(' +', ' ', element.strip().replace("\n","")))

# storing in dictionary
dicEmployeeContact = {'name': nameList1, 'designation': designationList1, 'email': emailList1, 'phoneNo': phoneList1, 'organization': companyList1, 'currentLocation': locationList1}

# for storing in CSV file 
df = pd.DataFrame(dicEmployeeContact) 
print(df)
#df.to_csv('employee_information.csv') # create a new file erasing the old data
df.to_csv('joyoct2020.csv', mode='a', header=False) # adding more data to the file 
browser.quit()
print ('file is ready')
    
