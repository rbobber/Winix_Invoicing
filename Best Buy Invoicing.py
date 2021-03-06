from selenium import webdriver
import time
import csv

driver = webdriver.Chrome()
driver.get("https://apps.commercehub.com/account/login?service=https://dsm.commercehub.com/dsm/shiro-cas")

driver.find_element_by_xpath('//input[@class="sign-in-input"]').send_keys("######")
driver.find_element_by_xpath('//input[@type="password"]').send_keys("###########")
driver.find_element_by_xpath('//input[@class="sign-in-button"]').click()
time.sleep(1)
driver.find_element_by_xpath("//a[contains(@href, '=bestbuy')]").click()

time.sleep(1)
driver.find_element_by_xpath("//a[contains(text(),'Needs Invoicing')]").click() #clicks on needs invoicing tab
time.sleep(1)
invoice_list = [] #itialize list of invoice numbers from a BAQ excel csv file
po_num_from_csv = [] #initialize list of PO numbers from a BAQ excel csv file

with open('sales to date.csv', 'r') as file: #opens csv file and adds all order data to lists
    reader = csv.DictReader(file)
    next(reader)
    print("\n")
    for line in reader:
        invoice_list.append(line['Invoice'])
        po_num_from_csv.append(line['PO'])
po_list = []
po_numbers = driver.find_elements_by_xpath('//a[@class="simple_link"]') #Finds every PO number on page, this will be the number of orders the program completes
for po_number in po_numbers:
    po_list.append(po_number.text)

count = 0
invoice_boxes = driver.find_elements_by_xpath('//input[@maxlength="22"]')
for invoice_box in invoice_boxes: #Fills in invoice number for each order on web form
    po = po_list[count]
    index = po_num_from_csv.index(po)
    # print(index)
    invoice = invoice_list[index]
    invoice_box.send_keys(invoice)
    count += 1

# Best Buy Net Days Due update from 30 to 45
items = driver.find_elements_by_xpath('//input[@value="30"]')
for item in items: #fills in item numbers for each order on web form
    item.clear()
    item.send_keys("45")


qtys = driver.find_elements_by_xpath('//td[@class="or_numericdata"]')
qty_list = []
count = 0
i = 0
j = 0
stop_flag = 0
i_value = 6

for qty in qtys:   #fills in quantities for all orders on web form
    count += 1
    i += 1
    if i == 2 and qty.text == '2':
        stop_flag = 1

    if stop_flag == 1 and i == 5:
        qty_list.append(qty.text)
        i = 0

    if j == 0 and i == 5 and stop_flag == 0: #only hits on the first invoice line
        j = 1
        i = 0
        print("hit 1")
        qty_list.append(qty.text)
    if i == i_value and stop_flag == 0:
        i = 0
        print("hit 2")
      # print(qty.text)
        # print("qty hit 2")
        qty_list.append(qty.text)
    if stop_flag == 1 and i == 0:
        stop_flag = 0  # resets stop flag after the end of the invoice line
        print("reset")

qty_boxes = driver.find_elements_by_xpath('//input[@maxlength="5"]')
count2 = 0
for qty_box in qty_boxes:
    qty_key = qty_list[count2]
    qty_box.send_keys(qty_key)
    count2 += 1

index = 1

time.sleep(60)

driver.close()
