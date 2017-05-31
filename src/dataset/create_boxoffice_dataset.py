def getAnswer(answer):
    gross_list=re.findall(r'^| gross.*',answer,re.I)
    print gross_list
    if len(gross_list) > 1:
        gross=""
        for item in gross_list:
            if re.search(r'INRConvert',str(item),re.I) != None:
                gross=re.findall(r'\|\d*.\d+\|\w',str(item),re.I)
        if len(gross) !=0:
            ans=gross[0].replace('|','').replace('b',' billion').replace('c',' cr').replace('m',' million')
            print "Gross = ",ans

        else:
            print "No info in DB"

    else:
        print "No info in DB"