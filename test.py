from datetime import datetime, date
import urllib.request # for downloading PDF
import PyPDF2 # for getting PDF into text
from io import BytesIO # for treating PDF as a file stream
import re # regex for parsing PDF

def build_breaks(cal_txt, cal_start):
    breaks = {
        'thanksgiving': {},
        'spring': {}
    }

    # remove random newlines
    cal_txt = cal_txt.rstrip()

    # build Thanksgiving
    
    # start
    # only extract the month and number
    messy_thanks = re.search("S\.C\.O\.T\.S\.\).*.,.*,....ThanksgivingBreakBegins", cal_txt, re.DOTALL).group(0)
    messy_thanks = re.search(",.*,", messy_thanks).group(0)

    # get the "November 2" between the commas, then split it by its space
    month_parts = re.split("\s", messy_thanks.split(',')[1])
    print(month_parts)
    month_number = datetime.strptime(month_parts[0][:3], '%b').month
        
    breaks['thanksgiving']['start'] = date(cal_start, month_number, int(month_parts[1]))

    # end
    messy_thanks = re.search("ofClasses).*.,.*,....ThanksgivingBreakEnds", cal_txt).group(0)
    messy_thanks = re.search(",.*,", messy_thanks).group(0)

    # get the "November 2" between the commas, then split it by its space
    month_parts = re.split("\s", messy_thanks.split(',')[1])
    # print(month_parts)
    month_number = datetime.strptime(month_parts[0], '%b').month
    
    breaks['thanksgiving']['end'] = date(cal_start+1, month_number, int(month_parts[1]))


cal_start = datetime.now().date().year
base_url = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-{}-{}.pdf"
cal_url = base_url.format(cal_start, cal_start % 2000 + 1) # i.e., 2017-18
cal_html = None

try:
    with urllib.request.urlopen(cal_url) as response:
        # this whole method is fairly fragile because the formatting could change in their PDF

        cal_html = response.read()

        # used the example from https://automatetheboringstuff.com/chapter13/
        calReader = PyPDF2.PdfFileReader(BytesIO(cal_html))

        # breaks are marked by SpringBreak{Begins,Ends} and
        # ThanksGivingBreak{Begins,Ends}

        # print(calReader.getPage(0).extractText())
        cal_txt = calReader.getPage(0).extractText()

        breaks = build_breaks(cal_txt, cal_start)


except urllib.request.URLError:
    print("mealplan: No connection to %s" % cal_url)
