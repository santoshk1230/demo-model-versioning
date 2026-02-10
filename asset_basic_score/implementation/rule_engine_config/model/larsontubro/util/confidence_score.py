import re
# import inflection
from larsontubro_1_0_0 import LARSONTUBRO_1_0_0 as rd
rule_dict = rd.get_rules()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

def camel_to_snake(camel_str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()

def is_numeric(column):
    try:
        float(column)
        return True
    except (ValueError, TypeError):
        return False
    
rule_dict2 = {k:v for k,v in rule_dict.items() if k!='base_score'}

min_max_scores = {}
score_to_cols = {}
score_cols = []

for k,v in rule_dict2.items():
    if '_tag' in k:
        continue
    score_cols.append(k)
    min_max_scores[k] = []
    score_to_cols[k] = []
    for k2,v2 in v.items():
        if isinstance(k2, tuple):
            score_to_cols[k].extend(list(k2))
        else:
            score_to_cols[k].append(k2)
            
        score_to_cols[k].extend(list(v2.keys()))
        for k3, v3 in v2.items():
            if isinstance(v3,list):
                for v4 in v3:
                    if isinstance(v4,list):
                        for v5 in v4:
                            if not is_numeric(v5) and not isinstance(v5,list):
                                score_to_cols[k].append(v5)
                
    for k2,v2 in v.items():
        for k3,v3 in v2.items():
            for v4 in v3:
                if isinstance(v4, list):
                    val = v4[-1]
                    if is_numeric(val):
                        min_max_scores[k].append(val)
                    elif isinstance(val, dict) and is_numeric(v4[-2]):
                        min_max_scores[k].append(v4[-2])


for k,v in score_to_cols.items():
    v3 = [v2 for v2 in v if not isinstance(v2,dict)]
    score_to_cols[k] = list(set(v3))
    if 'gst_advanced' in v:
        score_to_cols[k].extend(['trade_name','legal_name','mbr'])
    if 'phone_udyam' in v:
        score_to_cols[k].append('enterprise_name')
        
min_max_scores2 = {}
for k,v in min_max_scores.items():
    val = [v2 for v2 in v if int(v2)!=0]
    min_max_scores2[k] = []
    # if val:
    min_max_scores2[k].append(min(val))
    if min(val)!=max(val):
        min_max_scores2[k].append(max(val))
        
ind_triggers = list(min_max_scores2.keys())
        
# x = {'useCase': 'merchant-fraud', 'input': {'name': 'Ghanshyam Das Pinjani', 'phone': '9754028778', 'pan': 'AIQPP8942C', 'email': 'pinjaninikhil2@gmail.com', 'requestId': 'c36cb7bb-4c68-4f23-9fd7-ac1f215d7044'}, 'response': {'mutualFund': {'amcCount': None}, 'phoneSocial': {'flipkart': True, 'whatsapp': True, 'isWABusiness': True, 'indiamart': False, 'instagram': True, 'paytm': True}, 'phoneVpa': {'name': 'NIKHIL  PINJANI', 'upi': True}, 'enrichedData': {'riskyFintechCount': 0, 'phoneEmailMatch': True, 'phoneNameFirstSeenYear': None, 'phoneFirstSeenYear': 2017, 'diffPhoneNameCount': 3}, 'panVerification': {'name': 'GHANSHYAM DAS PINJANI', 'email': 'ha************da@yahoo.in', 'phoneNumber': None, 'aadharLinked': True}, 'cdsl': {'cdsl': None}, 'mobileUan': {'uanAvailable': True}, 'uanEPFO': {'dojEPF': '2017-10-01', 'doeEPF': '2018-05-17'}, 'dinDetails': {'din': False}, 'phoneUdyam': {'udyam': False, 'data': []}, 'gstAdvanced': {'data': [{'gstin': '23AIQPP8942C1Z0', 'tradeName': 'TOYOTA MOBILES', 'legalName': 'GHANSHYAM DAS PINJANI', 'mbr': []}]}}, 'clientName': 'pinelabs', 'mVersion': '2.0.0'}

def get_failed_trigger_range(x):
    min_val, max_val, err_range_diff_total, range_diff_total = 0, 0, 0, 0
    for c in ind_triggers:
        if isinstance(score_to_cols[c], list) or isinstance(score_to_cols[c], tuple):
            cols = [col for col in score_to_cols[c] if col in x.keys()]
            err = [1 if x[col]=='Error' else 0 for col in cols]
        else:
            col = score_to_cols[c]
            if x[col]=='Error':
                err = [1]
            else:
                err = [0]
        if sum(err)>0:
            if len(min_max_scores2[c])>1:
                min_val+=min_max_scores2[c][0]
                max_val+=min_max_scores2[c][1]
                range_diff = abs(min_max_scores2[c][1] - min_max_scores2[c][0])
            elif min_max_scores2[c][0]<0:
                min_val+=min_max_scores2[c][0]
                range_diff = abs(min_max_scores2[c][0])
            else:
                max_val+=min_max_scores2[c][0]
                range_diff = abs(min_max_scores2[c][0])
            err_range_diff_total = err_range_diff_total + range_diff
        if len(min_max_scores2[c])>1:
            range_diff = abs(min_max_scores2[c][1] - min_max_scores2[c][0])
        elif min_max_scores2[c][0]<0:
            range_diff = abs(min_max_scores2[c][0])
        else:
            range_diff = abs(min_max_scores2[c][0])
        range_diff_total = range_diff_total + range_diff
    return (min_val, max_val, err_range_diff_total, range_diff_total)
        
def get_confidence_score(transformed_payload):
    x = transformed_payload['response']
    for k,v in transformed_payload['input'].items():
        x['input_'+k] = v
    x2 = {}
    for k,v in x.items():
        if isinstance(v,dict):
            for k2,v2 in v.items():
                if isinstance(v2, list) and len(v2)>0:
                    for k4,v4 in v2[0].items():
                        x2[k4] = []
                    for k4 in v2:
                        for k5,v5 in k4.items():
                            if isinstance(v5, list):
                                x2[k5].extend(v5)
                            else:
                                x2[k5].append(v5)
                # else:
                #     for k3,v3 in v2.items():
                #         x2[k3] = v3
                # elif k2 not in x2:
                #     x2[k2] = v2
                elif k=='panVerification':
                    x2['pan_'+k2] = v2
                elif k=='phoneVpa':
                    if k2=='upi':
                        x2['vpa_available'] = v2
                    else:
                        x2['phone_vpa_'+k2] = v2
                else:
                    # x2[k+'.'+k2] = v2
                    x2[k2] = v2
        else:
            x2[k] = v

    x3 = {}
    for k,v in x2.items():
        if isinstance(v,list):
            # x3[inflection.underscore(k)] = [', '.join(v)]
            x3[camel_to_snake(k)] = [', '.join(v)]
        else:
            x3[camel_to_snake(k)] = [v]
    x4 = {}
    for k,v in x3.items():
        if None in v:
            x4[k] = 'Error'
        else:
            x4[k] = v

    failed_trigger_range = get_failed_trigger_range(x4)
    err_range_diff_total = failed_trigger_range[2]
    range_diff_total = failed_trigger_range[3]

    conf_score = ((range_diff_total-err_range_diff_total)/range_diff_total)*100.0
    confidence_score = round(conf_score,2)
    return confidence_score