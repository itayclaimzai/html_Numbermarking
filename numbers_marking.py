import pandas as pd
import re
import glob
from bs4 import BeautifulSoup


reg_num_text="<mm>place_holder</mm>"
date_text = "<dmm>place_holder</dmm>"
side_text= "<smm>place_holder</smm>"
money_text= "<monym>place_holder</monym>"
percent_text= "<perm>place_holder</perm>"
mypath='C:/Users/Itay0/Desktop/PythonProject/pdfonly/inputs/new_query/*.csv'
style_text = "<style> mm{background: #ffde80; direction: ltr;} dmm{background: aquamarine; direction: ltr;}" \
             "  smm{background: #dfdfd3; direction: ltr;} body{width: 90%; margin: 5%;}" \
             "monym{background: #6af16a; direction: ltr;} perm{background: #ff6cf4; direction: ltr;}</style>"
def textcehk(txin):
    tempi=txin
    lss = txin.replace("-"," ").split()
    for i in range(len(lss)):
        name=lss[i]
        if '₪' in name:
            money_text1 = money_text.replace('place_holder', lss[i - 1])
            tempcoon = money_text.replace('place_holder', name)
            tempi = tempi.replace(name, tempcoon).replace(lss[i - 1], money_text1)
            return tempi
        tempname = name.replace("-"," ").replace(".","").replace(",","").replace('%','').replace(" ","").replace("\\","").replace("/","")
        if str(tempname).isdecimal():
            dots=name.count(".")
            backslashes=name.count("\\")
            slashes = name.count("\\")
            totcheck=dots+backslashes+slashes

            if '%' in name :
                tempcoon = percent_text.replace('place_holder', name)
                tempi = tempi.replace(name,tempcoon)
                return tempi
            if totcheck==1:
                return tempi
                # tempcoon = side_text.replace('place_holder', name)
            else:
                if totcheck>1:
                    return tempi
                    # tempcoon = date_text.replace('place_holder', name)
                else:
                    return tempi
                    # tempcoon = reg_num_text.replace('place_holder', name)
            tempi=tempi.replace(name,tempcoon)

    print()
    return tempi


def checking(txin):
    tempi = txin
    lss = txin.split()
    for i in range(len(lss)):
        name=lss[i]
        if '₪' in name or 'ש"ח' in name:
            money_text1 = money_text.replace('place_holder', lss[i - 1])
            tempcoon = money_text.replace('place_holder', name)
            tempi = tempi.replace(name, tempcoon).replace(lss[i - 1], money_text1)
        if '%' in name:
            tempcoon = percent_text.replace('place_holder', name)
            tempi = tempi.replace(name, tempcoon)
    return tempi

onlyfiles=glob.glob(mypath)
outpath = 'htmls/'
for pathh in onlyfiles:
    dff=pd.read_csv(pathh)
    for i in range(len(dff)):
        try:
            df=dff.iloc[i]
            num= pathh.split("_")[-1]
            htmltext=df['htmltext']
            htmltext=style_text+htmltext
            case = df['case_number']
            name=case+'.html'
            filename = outpath+name
            soup = BeautifulSoup(htmltext, 'html.parser')
            alltasgs=soup.find_all('span')
            for tag in alltasgs:
                checktext=tag.text
                tag.string=checktext
                if '₪' in checktext or '%' in checktext:
                    chicki = checking(checktext)
                    tag.string.replace_with(chicki)

            outtext=str(soup)
            outtext=outtext.replace("&gt;",">")
            outtext = outtext.replace("&lt;", "<")
            f=open(filename,'w')
            f.write(outtext)
            f.close()
            print(num,' ',str(len(df)))
        except:
            pass


