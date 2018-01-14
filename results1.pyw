import requests
from bs4 import BeautifulSoup
import pandas
def results(sem,sec,join):
    payload = {
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"/wEPDwULLTE3MTAzMDk3NzUPZBYCAgMPZBYCAgcPDxYCHgRUZXh0ZWRkZKKjA/8YeuWfLRpWAZ2J1Qp0eXCJ",
            "__VIEWSTATEGENERATOR":"65B05190",
            "__EVENTVALIDATION":"/wEWFAKj/sbfBgLnsLO+DQLIk+gdAsmT6B0CypPoHQLLk+gdAsyT6B0CzZPoHQLOk+gdAt+T6B0C0JPoHQLIk6geAsiTpB4CyJOgHgLIk5weAsiTmB4CyJOUHgKL+46CBgKM54rGBgK7q7GGCLOsGLAxgUwycOU5mDizjY4EVXof",
            "cbosem":"1",
            "txtreg":"1210314401",
            "Button1":"Get Result"
            }
    try:
        base = join[0:8]
        try:
            payload['cbosem'] = sem
            result = []
            for roll in range(1,68):
                try:
                    if 1<=roll<=9:
                        payload['txtreg']=base+"0"+str(roll)
                    else:
                        payload['txtreg']=base+str(roll)
                    res = requests.post("https://doeresults.gitam.edu/onlineresults/pages/Newgrdcrdinput1.aspx", data=payload)
                    soup = BeautifulSoup(res.text,"html.parser")
                    name = soup.find("span",{"id":"lblname"}).text
                    reg = soup.find("span",{"id":"lblregdno"}).text
                    heads=[]
                    heads.append("Name")
                    heads.append("Roll No")

                    sgpa=soup.find("span",{"id":"lblgpa"}).text
                    cgpa=soup.find("span",{"id":"lblcgpa"}).text
                    table=soup.find("table",{"class":"table-responsive"})
                    rows=table.find_all("tr")[1:]
                    temp = []
                    temp.append(name)
                    temp.append(reg)
                    for row in rows:
                        count=0
                        for i in row.findAll("td"):
                            if count==3:
                                temp.append(i.text)
                            elif count==1:
                                heads.append(i.text)
                            count=count+1
                    temp.append(sgpa)
                    temp.append(cgpa)
                    result.append(temp)
                except:
                    pass
            heads.append("SGPA")
            heads.append("CGPA")
            df=pandas.DataFrame(result,index=None)
            num = join[5:7]
            n = int(num)+4
            file_name = "Year("+num+"-"+str(n)+")Sec-"+sec+"-Sem-"+sem+"-Results.csv"
            df.to_csv(file_name,header= heads,index=False)
            return True
        except:
            return False
    except:
        return False
