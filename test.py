from datetime import datetime, date
import urllib.request # for downloading PDF
import PyPDF2 # for getting PDF into text
from io import BytesIO # for treating PDF as a file stream
import re # regex for parsing PDF

def build_break_date(cal_txt, re_begin, re_end, yr_offset=0):
    # remove newlines
    cal_txt = re.sub(r"\r|\n", "", cal_txt)
    # print(cal_txt[:100])

    # only extract the month and number
    try:
        messy_thanks = re.search("{}.*.,.*,....{}".format(re_begin, re_end), \
                                 cal_txt, re.DOTALL).group(0)
    except AttributeError:
        print("build_break_date: building break with `{}` and `{}` failed".format(re_begin, re_end))
        return
        # exit(-1)
    # print(messy_thanks)

    messy_thanks = re.search(r",.*,", messy_thanks, re.DOTALL).group(0)

    # get the "November 2" between the commas, then split it by its space
    month_name = re.search(r"([a-z]|[A-Z])*", messy_thanks.split(',')[1]).group(0)
    day = re.search(r"\d+", messy_thanks).group(0)
    # print(messy_thanks.split(',')[1],"||||",month_name, day)
    # print(month_parts)
    month_number = datetime.strptime(month_name[:3], '%b').month

    return date(cal_start+yr_offset, month_number, int(day))


def build_breaks(cal_txt, cal_start):
    breaks = {
        'thanksgiving': {},
        'spring': {}
    }


    # build Thanksgiving break
    # The parentheses might not read correctly
    breaks['thanksgiving']['start'] = build_break_date(cal_txt, "ThanksgivingBreakBegins\(?CloseofClasses\)?", "ThanksgivingBreakEnds")
    breaks['thanksgiving']['end'] = build_break_date(cal_txt, \
                    "ThanksgivingBreakEnds\(?ClassesResume8:00am\)?", "LastDayofClass")

    # build Spring break
    breaks['spring']['start'] = build_break_date(cal_txt, "SpringBreakBegins\(?CloseofClasses\)?", "SpringBreakEnds", 1)
    breaks['spring']['end'] = build_break_date(cal_txt, \
                    "SpringBreakEnds\(?ClassesResume8:00am\)?", "LastDaytoWithdraw", 1)
    

    print(breaks)
    return breaks


cal_start = datetime.now().date().year
base_url = "http://www.edinboro.edu/directory/offices-services/records/academic-calendars/Academic-Calendar-{}-{}.pdf"
cal_url = base_url.format(cal_start, cal_start % 2000 + 1) # i.e., 2017-18
cal_html = None

try:
    with urllib.request.urlopen(cal_url, timeout=2) as response:
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
