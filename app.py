from flask import Flask,jsonify,request
import os.path
import subprocess
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import ast
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from fpdf import FPDF 
from os import path
from flask_pymongo import PyMongo




app = Flask(__name__)


def root_dir():
    return os.path.abspath(os.path.dirname('chromedriver'))







@app.route("/tneb-pdf-and-aws-txt_info",methods=['GET']) 
def home():
    response = requests.get('https://tneb-aws-pdf-download.herokuapp.com/viewBucketList')
    data = response.json()
    if len(data['result']) ==5:
         #path_main=['/home/assassincreed/Documents/tneb_payment_bill']
         #user_credential_txt=open("/home/assassincreed/Documents/tneb_user_credential")
         #user_credential_read=user_credential_txt.read()
         #user_credential=ast.literal_eval(user_credential_read)
         chrome_options = Options()
         chrome_options.add_argument("--headless")
         chrome_options.add_argument("--window-size=1920x1080")
         
         Aws_driver =webdriver.Chrome(executable_path='/static/chromedriver') 
         #executable_path=os.path.join(root_dir(),'chromedriver')             
         Aws_driver.get('https://www.amazon.in/')
         Aws_driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/span').click()
         Aws_mail_or_number=Aws_driver.find_element_by_xpath('//*[@id="ap_email"]')
         Aws_mail_or_number.send_keys(data['result']['Aws_user_login_id_or_phone_number'])
         Aws_driver.find_element_by_xpath('//*[@id="continue"]').click()
         Aws_user_password=Aws_driver.find_element_by_xpath('//*[@id="ap_password"]')
         Aws_user_password.send_keys(data['result']['Aws_password'])
         Aws_driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
         Aws_driver.find_element_by_xpath('//*[@id="nav-xshop"]/a[1]').click()
         time.sleep(2)
         Aws_driver.find_element_by_xpath('//*[@id="Electricity"]/span/a/div[2]/span').click()
         time.sleep(2)
         Aws_driver.find_element_by_xpath('//*[@id="a-autoid-0-announce"]').click()
         time.sleep(1)
         Aws_driver.find_element_by_xpath('//*[@id="ELECTRICITY_24"]').click()
         time.sleep(3)
         Aws_consumer_number=Aws_driver.find_element_by_xpath('//*[@id="Consumer Number"]')
         Aws_consumer_number.send_keys(data['result']['Aws_consumer_number'])
         Aws_driver.find_element_by_xpath('//*[@id="fetchBillActionId"]').click()
         time.sleep(5)
         detail_scr= BeautifulSoup(Aws_driver.page_source, 'html5lib')
         payment_detail=detail_scr.find_all("div",{"class": "a-section a-padding-medium"})
         Aws_payment_info=payment_detail[0].text
         
         
         driver = webdriver.Chrome(executable_path='/static/chromedriver')
         driver.get('https://www.tnebnet.org/awp/login')
         mail_or_number=driver.find_element_by_xpath('//*[@id="userName"]')
         mail_or_number.send_keys(data['result']['user_id'])
         user_password=driver.find_element_by_xpath('//*[@id="password"]')
         user_password.send_keys(data['result']['tneb_password'])
         driver.find_element_by_xpath('//*[@id="lin"]/table/tbody/tr/td[1]/table/tbody/tr[6]/td/input').click()
         time.sleep(3)
         driver.find_element_by_xpath('//*[@id="header1"]/div/table/tbody/tr[3]/td/label/a[3]').click()
         time.sleep(1)
         driver.find_element_by_xpath('//*[@id="form:j_idt114:0:j_idt131"]/span[1]').click()
         time.sleep(3)
         link_scr= BeautifulSoup(driver.page_source, 'html5lib')
         payment_detail=link_scr.find_all("tbody",{"id": "form:tbl_data"})
         row_count=len(payment_detail[0].find_all("tr"))
         #for link_no in range(0,row_count):
         driver.find_element_by_xpath('//*[@id="form:tbl:'+str(0)+':j_idt116"]/span[1]').click()
         time.sleep(3)
         ebbill= BeautifulSoup(driver.page_source, 'html5lib')
         bill_heading_table=ebbill.find('table',attrs={"width":"100%"})
         bill_heading_row=bill_heading_table.find_all('td')
         bill_info_table=ebbill.find('table',attrs={"cellpadding":"4"})  
         bill_info_row=bill_info_table.find_all('td')
         bill_header=list(filter(None, [ho.get_text() for ho in bill_heading_row]))
         
         def Convert(lst): 
                res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
                return res_dct 
                
         bill_text=Convert(list(filter(None, [ho.get_text() for ho in bill_info_row])))
         bill_dic=dict(bill_text)
         bill_text_pair=[dd+' '+kk for dd,kk in bill_text.items()]
         bill=bill_header+bill_text_pair
         pdf = FPDF()    
         pdf.add_page() 
         pdf.set_font("Arial", size = 15) 
         
         for gg in bill:
            pdf.cell(200, 10, txt = gg,  ln = 1, align = 'C') 
            
         
         pdf.output('/customer_id'+"/tneb_bill_of_"+bill_dic['Bill Month/Year:'].replace('/','_')+".pdf")
         Aws= open('/customer_id'+"/Amazon_payment_info.txt", "w")
         Aws.write(Aws_payment_info)
         Aws.close()
         Aws_driver.close()
         driver.close()
         return jsonify({'result':bill_text})
    else:
         check_list=['user_id','tneb_password','Aws_user_login_id_or_phone_number','Aws_password','Aws_consumer_number']
         given_list=list(data['result'].keys())
         miss_value=[keys for keys in check_list if keys not in given_list]
         if miss_value:
               return jsonify({'parameter not given':miss_value})
         else:
               return jsonify({'error with python code':'time-sleep'})
            
                   	            
 
if __name__ == "__main__":
    app.run(debug=True)
    

