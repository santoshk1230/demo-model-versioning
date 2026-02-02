def get_tag_dict(d):
    x = {}
    for i, j in d.items():
        for k, l in j.items():
            x[k] = l
    dic = {}
    if 'badUglyMatchFound' in x and isinstance(x['badUglyMatchFound'], str) and x.get('badUglyMatchFound').upper()=='UGLY':
        dic['BLCU01'] = True
    if 'riskyFintechCount' in x and isinstance(x['riskyFintechCount'], int) and x.get('riskyFintechCount') > 0:
        dic['REDI04'] = True
    if 'phoneDeactivatedDays' in x and isinstance(x, int):
        if x.get('phoneDeactivatedDays') < 200:
            dic['VITE04'] = True    
        elif x.get('phoneDeactivatedDays') < 400:
            dic['VITE01'] = True
    # dic['REDI05'] = False
    try:
        if 'inactiveGstCount' in x and isinstance(x['inactiveGstCount'], int) and x.get('inactiveGstCount') > 0 and isinstance(x['activeGstCount'], int) and x.get('activeGstCount', 0)==0:
                dic['VEDP04'] = True
        elif 'activeGstCount' in x and isinstance(x['activeGstCount'], 0) and x.get('activeGstCount') > 0:
            dic['VEDP01'] = True
    except:
        pass
    # dic['VALO03'] = False
    if x.get('numberBillingType', 0) == 'postpaid':
        dic['VATE72'] = True
    if x.get('udyamCount', 0):
        dic['VEDP02'] = True
    if x['phoneEmailFirstSeenYear'] is None:
        dic['VEID01'] = True
    if 'phoneNameFirstSeenYear' in x:
        if x['phoneNameFirstSeenYear'] is not None and x['phoneNameFirstSeenYear']!='':
            pnFirstSeenYear = 2025 - int(x['phoneNameFirstSeenYear'])
            if pnFirstSeenYear >= 5 and pnFirstSeenYear<10:
                dic['VIID71'] = True
            if pnFirstSeenYear >=10:
                dic['VIID72'] = True
    if 'phoneFirstSeenYear' in x:
        if x['phoneFirstSeenYear'] is not None and x['phoneFirstSeenYear']!='':
            pFirstSeenYear = 2025 - int(x['phoneFirstSeenYear'])
            if pFirstSeenYear >=10:
                dic['VITE71'] = True
            elif pFirstSeenYear>=6:
                dic['VITE72'] = True
            elif pFirstSeenYear>=4:
                dic['VITE73'] = True
    if x['upi']:
        dic['REDP72'] = True
    else:
        dic['REDI09'] = True
    if 'phoneUniquePincodesCount' in x and x['phoneUniquePincodesCount'] is not None and x['phoneUniquePincodesCount'] > 3:
        dic['VALO02'] = True

    return dic