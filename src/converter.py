
# coding: utf-8

# In[30]:

import csv
import itertools
import string


# From the csv file there is two row one is keymain which is the trans-unit id list and keyvalue is the translation value for the target tag inside of trans-unit tag. In following it will import the csv file and make a dictionary with the key and value of the file for accessing value by the trans-unit id later.
# We will later set the target language of translation in tarlan variable like 'en' is for English.
# 
# More about language https://tranpy.readthedocs.io/en/translate.bitdefender.com/file_formats/xliff.html#language-codes

# In[13]:

keylist = []
strmap = {}
with open('demo.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
            keylist.append(row['keymain'])
            index = row['keymain']
            strmap[index] = row['keyvalue']
tarlan = 'es'


# In[15]:

strmap = dict(map(lambda (key, value):(string.lower(key),value),strmap.items()))


# We will import the base xliff file which has proper trans-unit tags with id and source and target tag inside it.

# In[16]:

from lxml import etree
doc = etree.parse('demo.xliff')
docroot = doc.getroot()


# Setting all the files of xliff target language to translation language key.

# In[17]:

for child in docroot:
    child.attrib['target-language'] = tarlan


# Here in the loop we find out the child tag of trans-unit and get the id in cid variable and get the expected translation value from the strmap dictionary. Then checking the value exist and replace the target value with the translation value.
# Here 0 index is source tag and 1 index is target tag if all the trans-unit tag have these both tags inside either empty or with data.

# In[53]:

count  = 0
for child in docroot:
    for childs in child:
        for ch in childs:
            if ch.get('id') is not None:
                cid = ch.get('id').encode("utf-8")
                if cid is not None and strmap.has_key(string.lower(cid)):
                    value = strmap[string.lower(cid)]
                    if value is not None:
                        ch[0].text = unicode(value, 'utf-8')
                        count += 1
doc.write("output.xliff",encoding="utf-8", xml_declaration=True)

