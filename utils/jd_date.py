import datetime

def jd_today(top_date):
    today = datetime.date.today()
    if(top_date):
        top_dates = top_date.split('-')
        if(len(top_dates)==3):
            try:
                y = datetime.date(int(top_dates[0]),int(top_dates[1]),int(top_dates[2]))
            except:
                pass
            else:
                if(y>today):
                    today = y    
    return today