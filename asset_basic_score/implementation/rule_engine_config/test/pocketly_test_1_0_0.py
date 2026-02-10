import pytest
import pandas as pd
import sys

sys.path.append("rule_engine_config")
from rule_engine_config.model.pocketly.pocketly_1_0_0 import POCKETLY_1_0_0

sys.path.append("rule_engine")
from rule_engine.util.rule import get_score

rule_dict = POCKETLY_1_0_0.get_rules()


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ([150, ""], -50),
        ([250, ""], -50),
        ([590, ""], 50),
        ([610, ""], 80),
        (["", 200], -40),
        (["", 300], 20),
        (["", 410], 50),
        (["", 601], 140),
        (["", ""], -70),
    ],
)
def test_di_phonedi_combined_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["di_phonedi_combined_trigger_score"] = rule_dict[
        "di_phonedi_combined_trigger_score"
    ]
    score = get_score(
        {
            "digital_identity_score": input_value[0],
            "phone_name_d_i_score": input_value[1],
        },
        rule,
    )
    assert (
        score["ruleResponse"]["di_phonedi_combined_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        ("", 0),
        (2024, -40),
        (2023, 0),
        (2022, 10),
        (2020, 20),
        (2018, 30),
        (2012, 40),
        ("None", 0),
    ],
)
def test_phone_name_first_seen_year_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["phone_name_first_seen_year_trigger_score"] = rule_dict[
        "phone_name_first_seen_year_trigger_score"
    ]
    score = get_score({"phone_name_first_seen_year": input_value}, rule)
    assert (
        score["ruleResponse"]["phone_name_first_seen_year_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize(
    "input_value, expected", [(None, 0), (True, 0), (False, -30), ("error", 0)]
)
def test_has_flipkart_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["has_flipkart_trigger_score"] = rule_dict["has_flipkart_trigger_score"]
    score = get_score({"flipkart": input_value}, rule)
    assert score["ruleResponse"]["has_flipkart_trigger_score"]["score"] == expected


@pytest.mark.parametrize(
    "input_value, expected", [(None, 0), (True, 0), (False, -100), ("error", 0)]
)
def test_is_whatsapp_available_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_whatsapp_available_trigger_score"] = rule_dict[
        "is_whatsapp_available_trigger_score"
    ]
    score = get_score({"whatsapp": input_value}, rule)
    assert (
        score["ruleResponse"]["is_whatsapp_available_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize(
    "input_value, expected", [(None, 0), ("postpaid", 170), ("prepaid", 0)]
)
def test_is_postpaid_phone_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_postpaid_phone_trigger_score"] = rule_dict[
        "is_postpaid_phone_trigger_score"
    ]
    score = get_score({"number_billing_type": input_value}, rule)
    assert score["ruleResponse"]["is_postpaid_phone_trigger_score"]["score"] == expected


@pytest.mark.parametrize(
    "input_value, expected",  [(None, 0), (True, 50), (False, -30), ("Yes", 0)]
)
def test_vpa_available_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["vpa_available_trigger_score"] = rule_dict["vpa_available_trigger_score"]
    score = get_score({"vpa_available": input_value}, rule)
    assert score["ruleResponse"]["vpa_available_trigger_score"]["score"] == expected


@pytest.mark.parametrize("input_value, expected", [([None,None], 0),([0,1],0) ,([0,1], 0), ([1,1], -50), ([1,2],-50)])

def test_risky_fintech_ratio_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["risky_fintech_ratio_trigger_score"] = rule_dict[
        "risky_fintech_ratio_trigger_score"
    ]
    score = get_score(
        {
            "risky_fintech_count": input_value[0],
            "fintech_count": input_value[1],
        },
        rule,
    )
    assert (
        score["ruleResponse"]["risky_fintech_ratio_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected", [(None, 0), ("ugly", -500), ("bad", -300), ("Bad", -300)]
)
def test_is_ugly_bad_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_ugly_bad_trigger_score"] = rule_dict["is_ugly_bad_trigger_score"]
    score = get_score({"bad_ugly_match_found": input_value}, rule)
    assert score["ruleResponse"]["is_ugly_bad_trigger_score"]["score"] == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (["", "", ""], 0),
        (["", "", True], 0),
        (["", None, True], 0),
        ([None, "", True], 0),
        (["Tarun Shaikh", "Tarun Kumar", False], 0),
        (["Tarun", "Kumar", None], 0),
        (["Tarun", "Kumar", True], -40),
        (["abc", None, "abc"], 0),
        (["Tarun kumar Prajapati", "Tarun Prajapati", True], 100),
        (["Tarun Prajapati", "Tarun Kumar Prajapati", True], 100),
        (["Tarun Mishra", "Tarun Prajapati", True], 50),
        (["Tarun Kumar Prajapati", "Tarun Kumar Prajapati", True], 100),
    ],
)
def test_vpa_name_match_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["vpa_name_match_trigger_score"] = rule_dict["vpa_name_match_trigger_score"]
    score = get_score(
        {
            "input_name": input_value[0],
            "phone_vpa_name": input_value[1],
            "vpa_available": input_value[2],
        },
        rule,
    )
    assert score["ruleResponse"]["vpa_name_match_trigger_score"]["score"] == expected



@pytest.mark.parametrize(
    "input_value, expected",
    [
        (["", ""], 0),
        (["", ""], 0),
        (["", None], 0),
        ([None, ""], 0),
        (["Tarun Shaikh", "Tarun Kumar"], 50),
        (["Tarun", "Mitul"], -40),
        (["Tarun", "Kumar"], -40),
        (["abc", None], 0),
        (["Tarun kumar Prajapati", "Tarun Prajapati"], 100),
        (["Tarun Prajapati", "Tarun Kumar Prajapati"], 100),
        (["Tarun Mishra", "Tarun Prajapati"], 50),
        (["Tarun Kumar Prajapati", "Tarun Kumar Prajapati"], 100),
    ],
)
def test_pan_name_match_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["pan_name_match_trigger_score"] = rule_dict["pan_name_match_trigger_score"]
    score = get_score(
        {
            "pan_name": input_value[0],
            "input_name": input_value[1],
        },
        rule,
    )
    assert score["ruleResponse"]["pan_name_match_trigger_score"]["score"] == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        ("", 0),
        (2024, -40),
        (2023, 0),
        (2022, 10),
        (2020, 20),
        (2018, 30),
        (2012, 40),
        ("None", 0),
    ],
)
def test_email_first_seen_year_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["email_first_seen_year_trigger_score"] = rule_dict[
        "email_first_seen_year_trigger_score"
    ]
    score = get_score({"email_first_seen_year": input_value}, rule)
    assert (
        score["ruleResponse"]["email_first_seen_year_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        ("", 0),
        (2024, -40),
        (2023, 0),
        (2022, 10),
        (2020, 20),
        (2018, 30),
        (2012, 40),
        ("None", 0),
    ],
)
def test_phone_email_first_seen_year_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["phone_email_first_seen_year_trigger_score"] = rule_dict[
        "phone_email_first_seen_year_trigger_score"
    ]
    score = get_score({"phone_email_first_seen_year": input_value}, rule)

    assert (
        score["ruleResponse"]["phone_email_first_seen_year_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ([0, 0], -150),
        ([1, 1], 0),
        ([1, 0], 0),
        ([0, 1], 0),
        ([0, None], 0),
        ([None, 0], 0),
        ([None, None], 0),
        (["yes", None], 0),
        ([None, "no"], 0),
    ],
)
def test_is_whatsapp_flipkart_absent_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_whatsapp_flipkart_absent_trigger_score"] = rule_dict[
        "is_whatsapp_flipkart_absent_trigger_score"
    ]
    score = get_score({"flipkart": input_value[0], "whatsapp": input_value[1]}, rule)
    assert (
        score["ruleResponse"]["is_whatsapp_flipkart_absent_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize("input_value, expected", [(None, 0), (True, 70), (False, -90)])
def test_is_tax_payer_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_tax_payer_trigger_score"] = rule_dict["is_tax_payer_trigger_score"]
    score = get_score({"tax": input_value}, rule)
    assert score["ruleResponse"]["is_tax_payer_trigger_score"]["score"] == expected


@pytest.mark.parametrize("input_value, expected", [(None, 0), (True, 10), (False, 0)])
def test_is_whatsapp_business_available_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_whatsapp_business_available_trigger_score"] = rule_dict[
        "is_whatsapp_business_available_trigger_score"
    ]
    score = get_score({"is_w_a_business": input_value}, rule)
    assert (
        score["ruleResponse"]["is_whatsapp_business_available_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        ("2024-09-01", -100),
        ("2024-02-01", -60),
        ("2023-07-01", 0),
        ("2021-07-01", 70),
        ("2017-09-01", 100),
    ],
)
def test_phone_age_on_network_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["phone_age_on_network_trigger_score"] = rule_dict[
        "phone_age_on_network_trigger_score"
    ]
    score = get_score({"date_aon": input_value}, rule)
    assert (
        score["ruleResponse"]["phone_age_on_network_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [(None, 0), (1, 0), (2, 0), (7, -50), (12, -50), (False, 0), (0, 0), ("", 0)],
)
def test_has_multiple_email_with_phone_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["has_multiple_email_with_phone_trigger_score"] = rule_dict[
        "has_multiple_email_with_phone_trigger_score"
    ]
    score = get_score({"email_mapped_with_phone": input_value}, rule)
    assert (
        score["ruleResponse"]["has_multiple_email_with_phone_trigger_score"]["score"]
        == expected
    )


@pytest.mark.parametrize("input_value, expected", [(True, 10), (None, 0), (False, -10)])
def test_is_pan_email_present_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["is_pan_email_present_trigger_score"] = rule_dict[
        "is_pan_email_present_trigger_score"
    ]
    score = get_score({"pan_email_present": input_value}, rule)
    assert (
        score["ruleResponse"]["is_pan_email_present_trigger_score"]["score"] == expected
    )

### Adding test exclusive to pocketly

@pytest.mark.parametrize("input_value, expected",[("",0),(None,0),(5,-50),(39,0),(40,0),(79,20),(95,30)])
def test_indexed_name_match_trigger_score(input_value , expected):
    rule = {}
    rule['base_score'] = 450
    rule["indexed_name_match_trigger_score"] = rule_dict[
        "indexed_name_match_trigger_score"
    ]
    score = get_score({"indexed_name_match_score":input_value},rule)
    assert(
        score["ruleResponse"]["indexed_name_match_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        ("2004-09-01", 0),
        ("2024-02-01", -20),
        ("2023-09-01",-20),
        ("2015-12-03",-20),
        ("1980-01-01",0)
    ],
)
def test_age_limit_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["age_limit_trigger_score"] = rule_dict[
        "age_limit_trigger_score"
    ]
    score = get_score({"pan_birth_date": input_value}, rule)
    assert (
        score["ruleResponse"]["age_limit_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        (0, 0),
        (1, -20),
        (2,-40),
        (3,-60),
        (4,-80),
        (5,-100),
        (6,-100)
    ],
)
def test_inactive_gst_trigger_score(input_value, expected):
    rule = {}
    rule['base_score'] = 450
    rule["inactive_gst_trigger_score"] = rule_dict[
        "inactive_gst_trigger_score"
    ]
    score = get_score({"inactive_gst_count":input_value},rule)
    assert(
        score["ruleResponse"]["inactive_gst_trigger_score"]["score"] == expected
    )



@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, 0),
        (False, 0),
        (True,20)
    ],
)

def test_is_demat_trigger_score(input_value, expected):
    rule = {}
    rule['base_score'] = 450
    rule['is_demat_trigger_score']= rule_dict[
        "is_demat_trigger_score"
    ]
    score = get_score({"is_demat_available":input_value},rule)
    assert(
        score['ruleResponse']["is_demat_trigger_score"]["score"] == expected
    )


def test_pocketly_with_enriched_data():
    payload = {
        "enriched_data": {
            "name_match_score": 80,
            "email_first_seen_year": 2020,
            "phone_email_first_seen_year": 2021,
            "phone_name_first_seen_year": 2020,
            "email_mapped_with_phone": 1,
            "digital_identity_score": 600,
            "phone_name_d_i_score": 200,
            "fintech_count": 5,
            "risky_fintech_count": 1,
            "bad_ugly_match_found": "bad"
        },
        "phone_social": {
            "whatsapp": True,
            "flipkart": True,
            "is_w_a_business": False
        },
        "pan_verification_basic": {
            "tax": True,
            "pan_email_present": True,
            "name": "TEST",
            "dob": "1990-01-01"
        },
        "phone_vpa": {"upi": True, "name": "TEST"},
        "phone_intelligence": {"number_billing_type": "postpaid"},
        "age_on_network": {"date_aon": "2020-01-01"},
        "cdsl": {"cdsl": False},
        "gst": {"inactive_gst_count": 0}
    }

    result = get_score(payload, rule_dict)
    assert result is not None
