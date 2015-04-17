#################
### LIBRARIES ###
#################
import datetime
import random
import re
import mechanize
from bs4 import BeautifulSoup
import csv
from collections import deque

# Person object
# Genrates DOB, first and last name, & email adress,
class Person(object):

    #initialize the class by picking a birthday and gender
    def __init__(self):
        #These two are the seeds for all others.  
        self.__generate_birthday()
        self.__generate_female()

        #The rest are defined from the above
        self.__generate_SOB()
        self.__get_first_name()
        self.__get_last_name()

        print self.first_name, self.last_name, self.SOB, self.DOB

    #################################
    ### CHARACTERISTIC GENERATORS ###
    #################################
        
    #generate a birthday
    def __generate_birthday(self):       
        self.DOB = datetime.date(random.randint(1975,1986),random.randint(1,12),random.randint(1,31))

    #generate female indicator
    def  __generate_female(self):
        self.female = random.randint(1,10) != 4

    #generate the state of birth
    def __generate_SOB(self):
        rand = random.randint(1,79)
        if rand <= 55:
            self.SOB = "CT"
        else:
            if rand <= 65:
                self.SOB = "NY"
            else:
                if rand <= 69:
                    self.SOB = "MA"
                else:
                    if rand <= 70:
                        self.SOB = "ME"
                    else:
                        if rand <= 71:
                            self.SOB = "VT"
                        else:
                            if rand <= 72:
                                self.SOB = "RI"
                            else:
                                if rand <= 73:
                                    self.SOB = "NH"
                                else:
                                    if rand <= 74:
                                        self.SOB = "PA"
                                    else:
                                        if rand <= 75:
                                            self.SOB = "MD"
                                        else:
                                            if rand <= 76:
                                                self.SOB = "VA"                                        
                                            else:
                                                if rand <= 77:
                                                    self.SOB = "TX"
                                                else:
                                                    if rand <= 78:
                                                        self.SOB = "FL"
                                                    else:
                                                        if rand <= 79:
                                                            self.SOB = "NC"                                                        
    def __get_first_name(self):
        name_url = 'http://www.ssa.gov/OACT/babynames/state/index.html'

        # Set up the web browser from mechanize
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.addheaders = [('User-agent', 'Chrome')]

        response = br.open(name_url)
        #print response.read()

        #Print the forms on the page
        ##for form in br.forms():
        ##    print "Form Name:  ", form.name
        ##    # put the form name into a var
        ##    f = form.name
        ##    print form

        #select the apropriate form - the second one in the list
        br.form = list(br.forms())[1]


        #iterate through the controls
        ##for control in br.form.controls:
        ##    print control
        ##    print "type = %s, name = %s" % (control.type, control.name)


        # Grab the correct controls
        #state_control = br.form.find_control("state")
        #year_control = br.form.find_control("year")

        #list the keys, values in the state control
        ##if state_control.type == "select":
        ##    print "select"
        ##    for item in state_control.items:
        ##        print "name:  %s, values:  %s" % (item.name,str([label.text for label in item.get_labels()]))
        ##print state_control # lists the whole control, without values

        # set the controls
        br.form.set_value([self.SOB],"state")
        br.form.set_value([str((self.DOB.year))],"year")

        #get the page, pass it to soup
        response = br.submit()
        soup = BeautifulSoup(response)
        table = soup.find("table",width="72%")

        #declare results matricies
        #individual columns
        male_names = []
        male_nums = []
        female_names = []
        female_nums = []

        #digest each row of the name data, putting it into the names list
        for row in table.findAll('tr')[1:]:
            #get list of columns
            col = row.findAll('td')
            
            #digest the columns of each row, converting from unicode
            male_names.append(  re.sub(u'\xa0','',col[1].string).__str__())
            male_nums.append(int( re.sub(',','',re.sub(u'\xa0',"0",col[2].string).__str__() ) ))
            female_names.append(re.sub(u'\xa0','',col[3].string).__str__())
            female_nums.append(int(  re.sub(',','',re.sub(u'\xa0',"0",col[4].string).__str__() ) ))

        #choose wich array to examine
        if self.female :
            totals = female_nums
            names = female_names
        else:    
            totals = male_nums
            names = male_names
            
        #generate random number for indexing
        max = sum(totals)
        result = random.randint(1,max)

        #now select the name, based on the random number
        for i in range(0, len(totals)):
            if result >= totals[i]:
                result = result - totals[i]
            else:
                break

        self.first_name = names[i]        

    def __get_last_name(self):
        filepath = r'\Users\DKenefick\Desktop\Person\app_c.csv'
        
        #get the total
        cr = csv.reader(open(filepath,"rb"))
        lastline = deque(cr,1)[0]
        total = int(lastline[3])

        #generate the random number
        rnd = random.randint(1,total)

        #have to read in sequenialy anyway - just check as we read in.
        #change to seek?
        cr = csv.reader(open(filepath,"rb"))

        diff = total
        temp = 0
        lastname = ""
        #skip the header row
        next(cr,None)

        for line in cr:
            temp = abs(rnd - int(line[3]))
            if temp < diff:
                diff = temp
            else:
                self.last_name = line[0]
                break 
        
test = Person()
