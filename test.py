from datetime import datetime, date
import urllib.request # for downloading PDF
import PyPDF2 # for getting PDF into text
from io import BytesIO # for treating PDF as a file stream
import re # regex for parsing PDF

def build_break_date(cal_txt, re_begin, re_end, yr_offset=0):
    # only extract the month and number
    messy_thanks = re.search("{}.*.,.*,....{}".format(re_begin,re_end), \
                             cal_txt, re.DOTALL).group(0)
    # print(messy_thanks)

    messy_thanks = re.search(",.*,", messy_thanks, re.DOTALL).group(0)

    # get the "November 2" between the commas, then split it by its space
    month_parts = re.split("\s", messy_thanks.split(',')[1])
    # print(month_parts)
    month_number = datetime.strptime(month_parts[0][:3].rstrip(), '%b').month

    return date(cal_start+yr_offset, month_number, int(month_parts[1]))


def build_breaks(cal_txt, cal_start):
    breaks = {
        'thanksgiving': {},
        'spring': {}
    }

    # remove random newlines
    # this doesn't work for some reason so I have to use the re.DOTALL flag
    # cal_txt = str(cal_txt).rstrip()
    # this has newlines: (???)
    # print(cal_txt[:100].rstrip())

    # build Thanksgiving
    
    # start
    breaks['thanksgiving']['start'] = build_break_date(cal_txt, "S\.C\.O\.T\.S\.\)", "ThanksgivingBreakBegins")

    # end
    breaks['thanksgiving']['end'] = build_break_date(cal_txt, "ofClasses\)", "ThanksgivingBreakEnds")

    print(breaks)
    return breaks


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
