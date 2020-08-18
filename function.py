'''
VERIFICATION FUNCTION - NOT USED IN AUTOMATION FRAMEWORK
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''
#! /usr/bin/python

from bs4 import BeautifulSoup
import sys
import os


class Results:
    def __init__(self, file_name):
        self.file_name = file_name
        self.soup = None
        self.tables = []
        self.__create_soup()

    def __create_soup(self):

        fp = open(self.file_name,"r")
        content = fp.read()
        fp.close()
        self.soup = BeautifulSoup(content,"html.parser") #html5lib

    def get_paragraphs(self):
        self.paragraphs = self.soup.find_all("p")
        return self.paragraphs    

    def get_tables(self):
        self.tables = self.soup.find_all("table")
        return self.tables

    def get_column_names(self,table):
        column_names = [i.text for i in table.find_all("th")]
        return column_names

    def get_table_rows(self,table):
        return table.find_all("tr")

    def get_table_data(self,table_row,ignore=None):
        row_data = table_row.find_all("td")
        if row_data is not None:
            row = [data.text for data in row_data]
            return row
        else:
            return None


def get_value_from_para(file_name, str_com):
    """ Returns value for the <str_com> from main paragraph"""
    result = Results(file_name)
    result_paragraphs = result.get_paragraphs()

    for para_bs_tag in result_paragraphs:
        #para_str = str(para_bs_tag.text)
        para_str = para_bs_tag.text.encode('utf-8')

        if(para_str.find(str_com)>=0):

            if (str_com == "number of campaigns"):
                para_split = para_str.split(":")
                return para_split[1]
        
            elif(str_com == "unique assets"):
                para_split = para_str.split()
                par_split_colon = para_split[1].split(":")
                return par_split_colon[1]
        
            elif(str_com == "downloaded assets"):
                para_split = para_str.split()
                par_split_colon = para_split[4].split(":")
                return par_split_colon[1]

            elif(str_com == "deleted assets"):
                para_split = para_str.split()
                par_split_colon = para_split[7].split(":")                
                return par_split_colon[1]

            elif(str_com == "total assets"):
                para_split = para_str.split()
                return para_split[11]
    
    
    print("--------------------------------------------")
    print (" ", "Incorrect Argument -", str_com)
    print("--------------------------------------------")
    return None            

def get_value_from_row(file_name, header, unique_id, coloumn):
    """ Returns value from any row using above arguments"""
    """ example arguments - <filename> <Campaigns> <901> <House_Count> """
    campaign_found =0

    cdb_table = {"Campaigns":0, "CRTs":1, "Copy_Rotation":2, "Assets":3}

    tab_col = {'Campaigns'      :{"Camp_ID": 0, "Household Cap": 4, "Household Count":5, "Spacing": 7,    "Daily Cap":8, "Daily Count":9},
                'CRTs'          :{"Camp_ID": 0, "Expiration Date": 1,  "Deletion Time":2,    "Daily Count":3, "Household Count": 4},
                'Copy_Rotation' :{"Camp_ID": 0, "Order Number":5,  "Max Impressions":6,    "Used Impressions":7,    "Start Date":8, "End Date":9, "Last Shown": 10 }}

    if(tab_col.get(header,{}).get(coloumn) == None):
        print("Incorrect Arguments - ", header, unique_id, coloumn)
        sys.exit(0)
    else:
        col_idx = tab_col.get(header,{}).get(coloumn)
        
    for tab_idx in cdb_table:
        if(tab_idx == header):
            break

    res1 = Results(file_name)
    res1_tables = res1.get_tables()
    #column_names_1 = res1.get_column_names(res1_tables[cdb_table[tab_idx]])
    res1_table_rows = res1.get_table_rows(res1_tables[cdb_table[tab_idx]])
    
    for res1_row in res1_table_rows:
        data1 = res1.get_table_data(res1_row)
        
        if len(data1):
            if data1[0] == unique_id:
                campaign_found = 1    
                return data1[col_idx]
            
    if campaign_found !=1:
        print("------------------------------------")
        print (" ", "Argument",unique_id, "not found!")
        print("------------------------------------")
        sys.exit(0)


def get_value_under_table(file_name, header, str_com):
    '''Finds the value under specified table for a specific item and returns it's value'''
    '''<Header> <str_com> '''

    values_found=[]

    cdb_table = {"Campaigns":0, "CRTs":1, "Copy Rotation":2}

    for tab_idx in cdb_table:
        if tab_idx != header and str_com != "number of campaigns":
            print("Incorrect Arguments - ", header, str_com)
            sys.exit(0)

    res2 = Results(file_name)
    res2_para = res2.get_paragraphs()
    for para_bs_tag in res2_para:
        para_str = para_bs_tag.text.encode('utf-8')
        if para_str.find(str_com) >= 0 and str_com == "number of campaigns":
            para_split = para_str.split(":")
            values_found.append(para_split[1])

    if header == "Campaigns" :
        return values_found[1]
    if header == "CRTs":
        return values_found[2]
    if header == "Copy Rotation":
        return values_found[3]


def result_in_html(test_name, Previous_Data,Current_Data, Expected_Data):

    HTMLFILE = 'AdSmart Test result.html'
    f = open(HTMLFILE, "a+")
    
    table_data = []
    table_data.append([test_name, Previous_Data, Current_Data, Expected_Data, "Pass" if(Current_Data == str(Expected_Data)) else "Fail"])
    
    if (os.stat(HTMLFILE).st_size ==0):
        htmlcode = HTML.table(table_data,
        header_row =    ['Test Name', 'Previous Data', 'Current Data', 'Expected Data','Result'] ,
        col_width=      ['10%', '10%', '10%', '10%', '10%'],
        col_align=      ['left', 'center', 'center', 'center', 'center'],
        col_styles=     ['', '', '', '', 'background-color:green' if(Current_Data == str(Expected_Data)) else 'background-color:red' ])
    else:
        htmlcode = HTML.table(table_data,
        col_width=      ['10%', '10%', '10%', '10%', '10%'],
        col_align=      ['left', 'center', 'center', 'center', 'center'],
        col_styles=     ['', '', '', '', 'background-color:green' if(Current_Data == str(Expected_Data)) else 'background-color:red' ])
        
    f.write(htmlcode)
    #f.write(htmlcode + '<p>')
   
        
    f.close()


    

