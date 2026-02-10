import pytest
import pandas as pd
import sys

sys.path.append("rule_engine_config")
from rule_engine_config.model.fibe.fibe_1_0_0 import FIBE_1_0_0

sys.path.append("rule_engine")
from rule_engine.util.rule import get_score

rule_dict = FIBE_1_0_0.get_rules()

@pytest.mark.parametrize(
    "input_value, expected",
    [("", 0), (None, 0), (True, 20), (False, 0), ("False", 0)],
)
def test_cdsl_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["cdsl_trigger_score"] = rule_dict[
        "cdsl_trigger_score"
    ]
    score = get_score({"cdsl": input_value}, rule)
    assert score["ruleResponse"]["cdsl_trigger_score"]["score"] == expected

@pytest.mark.parametrize(
    "input_value, expected",
    [
        ([150, ""], -30),
        ([250, ""], -30),
        ([590, ""], -30),
        ([610, ""], 10),
        (["", 200], -30),
        (["", 300], -30),
        (["", 410], -30),
        (["", 601], 10),
        (["", ""], 0),
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
        (2025, -40),
        (2024, 0),
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
    "input_value, expected", [(None, 0), ("postpaid", 150), ("prepaid", 0)]
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
    "input_value, expected",  [(None, 0), (True, 50), (False, -20), ("Yes", 0)]
)
def test_vpa_available_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["vpa_available_trigger_score"] = rule_dict["vpa_available_trigger_score"]
    score = get_score({"vpa_available": input_value}, rule)
    assert score["ruleResponse"]["vpa_available_trigger_score"]["score"] == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (["", "", ""], 0),
        (["", "", True], 0),
        (["", None, True], 0),
        ([None, "", True], 0),
        (["Tarun Shaikh", "Tarun Kumar", False], 0),
        (["Tarun", "Kumar", None], 0),
        (["Tarun", "Kumar", True], -20),
        (["abc", None, "abc"], 0),
        (["Tarun kumar Prajapati", "Tarun Prajapati", True], 30),
        (["Tarun Prajapati", "Tarun Kumar Prajapati", True], 30),
        (["Tarun Mishra", "Tarun Prajapati", True], 10),
        (["Tarun Kumar Prajapati", "Tarun Kumar Prajapati", True], 30),
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
        (None, 0),
        ("", 0),
        (2025, -40),
        (2024, 0),
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
        (2025, -40),
        (2024, 0),
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


@pytest.mark.parametrize("input_value, expected", [(None, 0), (True, 70), (False, -50)])
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
        ("2024-09-01", -60),
        ("2024-02-01", -40),
        ("2023-07-01", 0),
        ("2021-07-01", 50),
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


def test_fibe_with_enriched_data():
    payload = {
        "enriched_data": {
            "name_match_score": 75,
            "email_first_seen_year": 2019,
            "phone_email_first_seen_year": 2020,
            "phone_name_first_seen_year": 2019,
            "email_mapped_with_phone": 1,
            "digital_identity_score": 580,
            "phone_name_d_i_score": 180,
            "fintech_count": 4,
            "risky_fintech_count": 0,
            "bad_ugly_match_found": "good"
        },
        "phone_social": {
            "whatsapp": True,
            "flipkart": False,
            "is_w_a_business": False
        },
        "pan_verification_basic": {
            "tax": True,
            "pan_email_present": True,
            "name": "TEST USER",
            "dob": "1992-05-10"
        },
        "phone_vpa": {"upi": True, "name": "TEST USER"},
        "phone_intelligence": {"number_billing_type": "prepaid"},
        "age_on_network": {"date_aon": "2019-06-01"},
        "cdsl": {"cdsl": False},
        "gst": {"inactive_gst_count": 0}
    }

    result = get_score(payload, rule_dict)
    assert result is not None
