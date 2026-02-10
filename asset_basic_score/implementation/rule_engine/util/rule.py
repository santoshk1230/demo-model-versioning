from datetime import date
from rapidfuzz import fuzz
import datetime
import re
from rule_engine.util.name_match import get_similarity_class
# from util.business_classifier import business_classifier
import operator
import traceback

operators = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}

current_year = (date.today()).year

# tag_dict = {
#     "Dubious Email": "df06",
#     "Not Present on Whatsapp and Other relavant digital Platforms": "df02",
#     "PAN not Registered on ITR": "df05",
#     "Phone Picked up less than 6 Months": "di02",
#     "Phone Picked up less than 1 Year": "di02",
#     "Name match with other Bank Accounts": "nm01",
#     "Name Partial Match with other bank Accounts": "nm01",
#     "Similar Bank Application with Different Name": "nm01",
#     "Same phone linked to more than 5 Email ids": "mi01",
#     "Reported By CUG": "bi01",
# }

tag_dict = {'ai01': 'Address Incomplete',
    'ai02': 'High Location Volatility - Multiple Address',
    'ai03': 'Address Incorrect',
    'ai06': 'Blacklisted Pincode',
    'ai04': 'Pncode Blacklisted by FI',
    'ai05': 'Migrant',
    'bf01': 'GST Inactive',
    'bf02': 'Active GST Found',
    'bf03': 'Udhyam Found',
    'bf04': 'GST Cancelled by tax Payer request',
    'bg01': 'FIR Found',
    'bg02': 'Wilful Dafaulter',
    'bg03': 'AML reporting Found',
    'bg04': 'Politically Exposed Personnel',
    'bg05': 'Court Cases',
    'bi01': 'Reported by CUG - Blacklisted',
    'bi02': 'Reported on cybercrime',
    'df01': 'No digital footprint presence found across platfroms (Phone)',
    'REDI02': 'Communication Platform Registration (Phone)',
    'REDI03': 'No Ecommerce registeration found (Phone)',
    'REDI04': 'UPI not found',
    'REDP02': 'No ITR found',
    'VADO01': 'Temporary Email',
    'REDI07': 'Registered on Risky Fintech',
    'df08': 'Invalid Phone Number',
    'df09': 'Porting History',
    'df10': 'Email Reputation',
    'df11': 'Found on Gambling Platfrom',
    'df13': 'Email Inbox not reachable',
    'df14': 'Digital Footprint Across Multiple Segments (Email)',
    'df15': 'Communication Platform Registration (Email)',
    'df16': 'ECommerce Registration (Email)',
    'di01': 'Low Digital Vintage on registration platfroms',
    'di02': 'Recycled Phone Number',
    'di03': 'Uan verification failed',
    'di04': 'Pan Details Mismatch',
    'di05': 'Pan Details Mismatch',
    'di06': 'Pan Details Mismatch',
    'di07': 'Investment Footprint Mismatch',
    'di08': 'Investment Footprint Mismatch',
    'di09': 'PAN not Seeded',
    'di10': 'Invalid PAN',
    'di11': 'Phone and Email not linked',
    'VITE03': 'Low Phone Vintage',
    'di13': 'Low Phone Vintage',
    'di14': 'Footprint Found on Phone but not on email.',
    'di15': 'Low Pan Vintage',
    'VIDI01': 'Low Email Vintage',
    'di17': 'Recycled Phone Number',
    'em01': 'No Current Employment Record Found',
    'em02': 'Current Employment Mismatch',
    'em03': 'Frequent Employment Change',
    'em04': 'Dubious Employer',
    'VEID02': 'Multiple identities against phone',
    'mi02': 'Multiple identities against email',
    'mi03': 'Multiple identities against phone',
    'mi04': 'Multiple identities against email',
    'VEDP16': 'Bank Name MisMatch',
    'nm02': 'Registration Name Match',
    'nm03': 'PAN Name MisMatch',
    'nm04': 'Bank and PAN Name MisMatch',
    'VEDP20': 'Bank Name Partial Match',
    'nm06': 'Pan Name Partial Match'}

def get_diff_in_months(ca, aon):
    try:
        aon_date = datetime.datetime.strptime(str(aon), "%Y-%m-%d")
    except:
        try:
            aon_date = datetime.datetime.strptime(str(aon), "%d-%m-%Y")
        except:
            return ((ca - aon) * 365.0) / 31.0

    current_date = datetime.datetime.today()

    months_diff = (current_date.year - aon_date.year) * 12 + (
        current_date.month - aon_date.month
    )
    return months_diff

def combined_rules(x, a, y, b):
    if isinstance(a,list) and isinstance(b,dict):
        operator = operators[list(b.keys())[0]]
        value = list(b.values())[0]
        return x in a and operator(y, value)
    elif isinstance(a,dict) and isinstance(b,list):
        operator = operators[list(a.keys())[0]]
        value = list(a.values())[0]
        return operator(x, value) and y in b
    elif isinstance(a,dict) and isinstance(b,dict):
        operator1 = operators[list(a.keys())[0]]
        value1 = list(a.values())[0]
        operator2 = operators[list(b.keys())[0]]
        value2 = list(b.values())[0]
        return operator1(x, value1) and operator2(y, value2)

def is_numeric(column):
    try:
        float(column)
        return True
    except (ValueError, TypeError):
        return False
    
def clean_phone(p):
    p1 = re.sub('^(\+?\(?0+\)?\W*)', '', str(p)).strip()
    if len(str(p1))>10:
        p1 = re.sub('^(\+?\(?91\)?\W*)','',str(p1)).strip()
    return p1

def is_phone(column):
    try:
        if len(str(int(float(column))).strip())==10:
            return True
        else: return False
    except (ValueError, TypeError):
        return False

comparison_operators = {
    "==": lambda x, y: (
        x in y if x is None else x.lower().strip() in y if not is_numeric(x) else x in y
    ),
    "!=": lambda x, y: x != y if x is not None else False,
    "<": lambda x, y: x < y if x is not None else False,
    ">": lambda x, y: x > y if x is not None else False,
    "<=": lambda x, y: x <= y if x is not None else False,
    ">=": lambda x, y: x >= y if x is not None else False,
    "between_1": lambda x, y, z: x < y <= z if x is not None else False,
    "between_2": lambda x, y, z: x <= y <= z if x is not None else False,
    "between_3": lambda x, y, z: x <= y < z if x is not None else False,
    "x_and_y": lambda x, a, y, b: x in a and y in b,
    "combined_rule": lambda x, a, y, b: combined_rules(x, a, y, b),
    "x_or_y": lambda x, a, y, b: x in a or y in b,
    "x_and_y_and_z": lambda x, a, y, b, z, c: x in a and y in b and z in c,
    "w_or_x_or_y_or_z": lambda w, a, x, b, y, c, z, d: w in a
    or x in b
    or y in c
    or z in d,
    "w_or_x_or_y_is_null_or_z_is_null": lambda w, a, x, b, y, z: w in a
    or x in b
    or y is None
    or z is None
    or y == None
    or z == None,
    "x*y": lambda x, y: x * y,
    "token_ratio": lambda n1, n2: (
        None
        if n1 is None or n2 is None
        else fuzz.partial_token_set_ratio(n1.lower(), n2.lower())
    ),
    "time_in_months": lambda ca, x: (
        get_diff_in_months(ca, x) if x is not None and x != "" else None
    ),
    "time_in_yrs": lambda ca, x: ca - x if x is not None and x != "" else None,
    # "empty_string_check": lambda x: str(x).strip() == "",
    "empty_string_check": lambda x: x == "",
    "null_check": lambda x: x is None or x == None or x in ["nan", "NaN"],
    "sequential_triggers": True,
    "numbers_count": lambda x: len(re.findall(r"\d", x)),
    "get_similarity_class": lambda x, y: get_similarity_class(x, y),
    # "get_business_flag": lambda x : business_classifier(x),
    "get_default_score": lambda x: x,
    "email_check": lambda x: "@" in str(x),
    "extract_domain": lambda x: str(x).split('@')[-1].lower().replace('.in','.com').replace('.co.in','.com').strip() if "@" in str(x) else "",
    "str_len_check": lambda x, v: len(str(x).replace('.com','').strip()) >= v if x != None else False,
    "clean_phone": lambda x: clean_phone(x),
    "phone_match": lambda x, y: (
        False
        if x == "" or y == ""
        else (
            str(int(x)).strip() == str(int(y)).strip()
            if is_phone(x) and is_phone(y)
            else False
        )
    ),
    "phone_unmatch": lambda x, y: (False if x == "" or y == "" else (str(int(x)).strip() != str(int(y)).strip() if is_phone(x) and is_phone(y) else False)),
    "x==y": lambda x, y: (False if x == "" or y == "" else (str(int(x)).strip() == str(int(y)).strip() if is_numeric(x) and is_numeric(y) else x.lower().strip() == x.lower().strip())),
    "x!=y": lambda x, y: (False if x == "" or y == "" else (str(int(x)).strip() != str(int(y)).strip() if is_numeric(x) and is_numeric(y) else x.lower().strip() != x.lower().strip())),
    "email_match": lambda x, y: (False if x == "" or y == "" else (str(x).lower().strip() == str(y).lower().strip() if not is_numeric(x) and not is_numeric(y) and '@' in str(x) and '@' in str(y) else False)),
    "email_unmatch": lambda x, y: (False if x == "" or y == "" else (str(x).lower().strip() != str(y).lower().strip() if not is_numeric(x) and not is_numeric(y) and '@' in str(x) and '@' in str(y) else False)),
    "max_trigger_score" : lambda x : max(x),
    "min_trigger_score" : lambda x : min(x)
}


def get_score(x, rule_dict):
    """
    Creates the trigger scores.
    Args:
        x : input dataset with all the raw columns for the triggers
        rule_dict : the dictionary that contains the rules for trigger creation

    Returns:
        A Series that when converted to a Dataframe gives the scores.
        Eg :
            df['trigger_scores'] = df.apply(lambda x : get_score(x, rule_dict), axis=1)
            score_df = pd.DataFrame(df['trigger_scores'].tolist())
    """

    final_score_dict = {}
    trigger_score_dict = {}
    final_tag_dict = {}
    functions = list(rule_dict.keys())
    failed_rules = []
    # print ('x :', x)
    for function in functions:
        if function == "base_score":
            trigger_score_dict["base_score"] = rule_dict["base_score"]
            continue
        for col, rules in rule_dict[function].items():
            if trigger_score_dict.get(function) == 0 or trigger_score_dict.get(
                function
            ):
                break
            if x.get("col_to_skip"):
                if col in x.get("col_to_skip"):
                    continue
            for rule in rules:
                try:
                    if trigger_score_dict.get(function) == 0 or trigger_score_dict.get(
                        function
                    ):
                        break
                    elif rule != "else":
                        operator = comparison_operators[rule]
                # except:
                except Exception as e:
                    traceback.print_exc()
                    failed_rules.append(function)
                    pass
                for rule_value in rules[rule]:
                    try:
                        if rule == "else":
                            continue
                        elif rule in ["token_ratio"]:
                            x[col] = operator(x[rule_value[0]], x[rule_value[1]])
                        elif rule in ["time_in_months", "time_in_yrs"]:
                            x[col] = operator(current_year, x[rule_value[0]])
                        elif rule in ["numbers_count","extract_domain","get_business_flag","clean_phone"]:
                            x[col] = operator(x[rule_value[0]])
                        elif rule in ["get_similarity_class"]:
                            # print ('rule_value :', rule_value)
                            x[col] = operator(x[rule_value[0]], x[rule_value[1]])
                        elif rule in ["get_default_score"]:
                            trigger_score_dict[function] = {
                                "score": operator(rule_value),
                                "type": "Success",
                            }
                            break
                        elif isinstance(col, tuple):
                            if rule in ['min_trigger_score','max_trigger_score']:
                                score_dict = {tg : trigger_score_dict[tg].get('score') for tg in col}
                                score_vals = [trigger_score_dict[tg].get('score') for tg in col]
                                agg_trigger_score = operator(score_vals)
                                agg_trigger = list(score_dict.keys())[list(score_dict.values()).index(agg_trigger_score)]
                                
                                trigger_score_dict[agg_trigger] = {
                                "score": agg_trigger_score,
                                "type": "Success"
                                }
                                triggers_to_remove = [tr for tr in score_dict if tr!=agg_trigger]
                                for tr in triggers_to_remove:
                                    trigger_score_dict.pop(tr, None)
                                break
                            elif rule in ["sequential_triggers"]:
                                x["col_to_skip"] = [c for c in col if x[c] == ""]
                                break
                            elif rule in ["x==y","x!=y","phone_match","phone_unmatch","email_match","email_unmatch"]:
                                if operator(x[col[0]], x[col[1]]):
                                    trigger_score_dict[function] = {
                                        "score": rule_value[0],
                                        "type": "Success",
                                    }
                                    break
                            elif rule in ["w_or_x_or_y_is_null_or_z_is_null"]:
                                if operator(
                                    x[col[0]],
                                    rule_value[0],
                                    x[col[1]],
                                    rule_value[1],
                                    x[col[0]],
                                    x[col[1]],
                                ):
                                    if isinstance(rule_value[-1], dict):
                                        final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                        score_idx = -2
                                    else:
                                        score_idx = -1
                                    trigger_score_dict[function] = {
                                        "score": rule_value[score_idx],
                                        "type": "Success",
                                    }
                                    break
                                else:
                                    continue
                            elif len(col) == 2 and len(rule_value) == 3:
                                if operator(
                                    x[col[0]], rule_value[0], x[col[1]], rule_value[1]
                                ):
                                    if isinstance(rule_value[-1], dict):
                                        final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                        score_idx = -2
                                    else:
                                        score_idx = -1
                                    trigger_score_dict[function] = {
                                        "score": rule_value[score_idx],
                                        "type": "Success",
                                    }
                                    break
                                else:
                                    continue
                            elif len(col) == 2 and len(rule_value) == 5:
                                if operator(
                                    x[col[0]],
                                    rule_value[0],
                                    x[col[1]],
                                    rule_value[1],
                                    x[col[0]],
                                    rule_value[2],
                                    x[col[1]],
                                    rule_value[3],
                                ):
                                    if isinstance(rule_value[-1], dict):
                                        final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                        score_idx = -2
                                    else:
                                        score_idx = -1
                                    trigger_score_dict[function] = {
                                        "score": rule_value[score_idx],
                                        "type": "Success",
                                    }
                                    break
                                else:
                                    continue
                            elif len(col) == 3:
                                if operator(
                                    x[col[0]],
                                    rule_value[0],
                                    x[col[1]],
                                    rule_value[1],
                                    x[col[2]],
                                    rule_value[2],
                                ):
                                    if isinstance(rule_value[-1], dict):
                                        final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                        score_idx = -2
                                    else:
                                        score_idx = -1
                                    trigger_score_dict[function] = {
                                        "score": rule_value[score_idx],
                                        "type": "Success",
                                    }
                                    break
                                else:
                                    continue
                        elif rule in ["x*y"]:
                            trigger_score_dict[function] = {
                                "score": operator(x[col], rule_value[0]),
                                "type": "Success",
                            }
                            break
                        elif rule in [
                            "null_check",
                            "empty_string_check",
                            "email_check"
                        ]:
                            if rule in [
                                "null_check",
                                "empty_string_check"
                            ] and operator(x[col]):
                                if isinstance(rule_value[-1], dict):
                                    final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                    score_idx = -2
                                else:
                                    score_idx = -1
                                trigger_score_dict[function] = {
                                    "score": rule_value[score_idx],
                                    "type": "Exception",
                                }
                                break
                            elif rule in ["email_check"] and operator(
                                x[col]
                            ):
                                if isinstance(rule_value[-1], dict):
                                    final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                    score_idx = -2
                                else:
                                    score_idx = -1
                                trigger_score_dict[function] = {
                                    "score": rule_value[score_idx],
                                    "type": "Success",
                                }
                                break
                            else:
                                continue
                        elif rule not in [
                            "between_1",
                            "between_2",
                            "between_3",
                            "else",
                            # "str_len_check"
                        ]:
                            if operator(x[col], rule_value[0]):
                                if isinstance(rule_value[-1], dict):
                                    final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                    score_idx = -2
                                else:
                                    score_idx = -1
                                trigger_score_dict[function] = {
                                    "score": rule_value[score_idx],
                                    "type": "Success",
                                }
                                break
                            else:
                                continue
                        elif rule in ["between_1", "between_2", "between_3"]:
                            if operator(rule_value[0][0], x[col], rule_value[0][1]):
                                if isinstance(rule_value[-1], dict):
                                    final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                                    score_idx = -2
                                else:
                                    score_idx = -1
                                trigger_score_dict[function] = {
                                    "score": rule_value[score_idx],
                                    "type": "Success",
                                }
                                break
                            else:
                                continue
                    # except:
                    except Exception as e:
                        traceback.print_exc()
                        failed_rules.append(function)
                        pass
            if trigger_score_dict.get(function) == None and "else" in rules.keys():
                try:
                    # print ('rule value :', rules[rule])
                    if isinstance(rules[rule][-1], dict):
                        final_tag_dict[list(rule_value[-1].keys())[0]] = list(rule_value[-1].values())[0]
                        score_idx = -2
                    else:
                        score_idx = -1
                    trigger_score_dict[function] = {
                        "score": rules[rule][score_idx],
                        "type": "Exception",
                    }
                # except:
                except Exception as e:
                    traceback.print_exc()
                    failed_rules.append(function)
                    pass
                break

    base_score = trigger_score_dict["base_score"]
    trigger_score_dict = {
        k: trigger_score_dict[k] for k in trigger_score_dict if k != "base_score"
    }

    # tag_values = [
    #     trigger_score_dict[k].get("score")
    #     for k in trigger_score_dict
    #     if "_tag" in k and trigger_score_dict[k].get("score") != "no tag"
    # ] + list(final_tag_dict.values())
    # tag_ids = [tag_dict.get(t) for t in tag_values]

    tag_ids = [
        trigger_score_dict[k].get("score")
        for k in trigger_score_dict
        if "_tag" in k and trigger_score_dict[k].get("score") != "no tag"
    ] + list(final_tag_dict.values())
    tag_values = [tag_dict.get(t) for t in tag_ids]
    
    trigger_score_dict = {
        k: trigger_score_dict[k]
        for k in trigger_score_dict
        if "_tag" not in k and trigger_score_dict[k].get("score") != "no tag"
    }
    final_score_dict["ruleResponse"] = trigger_score_dict
    final_score_dict["totalScore"] = (
        sum([trigger_score_dict[k].get("score") for k in trigger_score_dict])
        + base_score
    )
    final_score_dict["base_score"] = base_score
    final_score_dict["tags"] = tag_values
    final_score_dict["tag_ids"] = tag_ids
    skipped_rules = [
        t
        for t in functions
        if (t not in trigger_score_dict) and ("_tag" not in t) and (t != "base_score")
    ]
    final_score_dict["failed_rules"] = list(set(failed_rules + skipped_rules))
    print ('final_score_dict :', final_score_dict)
    return final_score_dict