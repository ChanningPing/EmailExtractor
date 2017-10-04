# -*- coding: utf-8 -*-
'''
Author: Qing Ping 10-03-2017
This script is used to extract emails from pdf files.
Replace <target_dir> with your own folder of pdf files, and execute the script to get list of emails
'''
import re
import textract
import os
import collections
import sys


reload(sys)
sys.setdefaultencoding('utf8')


def get_emails_merge(s):
    """Returns an iterator of matched emails found in string s."""
    regex1 = re.compile(("(\{[a-zA-Z0-9! \n#$%&',;*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*\}(@|\sat\s)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(\.|"
                        "\sdot\s))+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)"))

    return  (email[0] for email in re.findall(regex1, s) if not email[0].startswith('//'))


def get_emails(s):
    """Returns an iterator of matched emails found in string s."""

    regex2 = re.compile(("([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`"
                         "{|}~-]+)*(@|\sat\s)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(\.|"
                         "\sdot\s))+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)"))


    return (email[0] for email in re.findall(regex2, s) if not email[0].startswith('//'))

def get_emails_irregular(s):
    """Returns an iterator of matched emails found in string s."""

    regex2 = re.compile(("(\{[a-zA-Z0-9!@,; \n#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!@, #$%&'*+\/=?^_`"
                         "{|}~-]+)*(@|\sat\s)*[a-zA-Z0-9!@, #$%&'*+\/=?^_`{|}~-]+\}(?:[a-zA-Z0-9, ](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(\.|"
                         "\sdot\s))+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)"))


    return (email[0] for email in re.findall(regex2, s) if not email[0].startswith('//'))

def pdf_text(pdf_dir):
    text = ''
    try:
        text = textract.process(pdf_dir, encoding='utf-8')
    except Exception:
        print('------! ! ! file format issue:'+pdf_dir)
        pass  # or you could use 'continue'

    return text


def email_split(email_string):
    if "{" not in email_string and "}" not in email_string: return [email_string]
    emails = []
    email_string = email_string.split('{')[-1]
    if ',' in email_string.split('}')[0]:
        heads = email_string.split('}')[0].split(',')
    elif ';' in email_string.split('}')[0]:
        heads = email_string.split('}')[0].split(';')
    else:
        heads = email_string.split('}')[0].split(' ')
    tail = email_string.split('}')[-1]
    for head in heads:
        emails.append(head.strip()+tail)
    return emails



def extract_save_emails(target_dir):

    emails = []
    for file_name in os.listdir(target_dir):
        if '.pdf' not in file_name: continue
        print(target_dir + file_name)
        text = pdf_text(target_dir + file_name)
        local_emails = collections.defaultdict(int)
        #print(text)
        for email_string in get_emails_merge(text):
            for email in email_split(email_string):
                local_emails[email] += 1
        for email_string in get_emails(text):
            for email in email_split(email_string):
                local_emails[email] += 1
        for email_string in get_emails_irregular(text):
            for email in email_split(email_string):
                local_emails[email] += 1
        emails += local_emails.keys()
    f = open('data/' + target_dir.split('/')[-2] + '.txt', 'w')
    for email in emails:
        f.write(email+'\n')
    f.close()



if __name__ == "__main__":
    target_dir = '/Users/qingping/Documents/Conference_PDFs/BigDataSecurity_HPSC_IDS_2016/'
    extract_save_emails(target_dir)
    #for email in get_emails('hahah hahah {csyliu, csshzhong, cswjli}@comp.polyu.edu.hk hahah haha'):
        #print(email)




