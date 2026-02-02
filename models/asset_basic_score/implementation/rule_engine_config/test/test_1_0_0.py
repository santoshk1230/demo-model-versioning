import pytest
import pandas as pd
import sys

sys.path.append("rule_engine_config")
from model.Cholamandalam_1_0_0 import Cholamandalam_1_0_0

sys.path.append("rule_engine")
from util.rule import get_score

rule_dict = Cholamandalam_1_0_0.get_rules()


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ([150, ""], 0),
        ([250, ""], 20),
        ([590, ""], 50),
        ([610, ""], 80),
        (["", 200], -40),
        (["", 300], 20),
        (["", 410], 50),
        (["", 601], 80),
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
    "input_value, expected", [(None, 0), (True, 50), (False, -20), ("Yes", 0)]
)
def test_vpa_available_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["vpa_available_trigger_score"] = rule_dict["vpa_available_trigger_score"]
    score = get_score({"vpa_available": input_value}, rule)
    assert score["ruleResponse"]["vpa_available_trigger_score"]["score"] == expected


@pytest.mark.parametrize("input_value, expected", [(None, 0), (1, -50), (10, -50)])
def test_risky_fintech_ratio_trigger_score(input_value, expected):
    rule = {}
    rule["base_score"] = 450
    rule["risky_fintech_ratio_trigger_score"] = rule_dict[
        "risky_fintech_ratio_trigger_score"
    ]
    score = get_score({"risky_fintech_count": input_value}, rule)
    assert (
        score["ruleResponse"]["risky_fintech_ratio_trigger_score"]["score"] == expected
    )


@pytest.mark.parametrize(
    "input_value, expected", [(None, 0), ("ugly", -300), ("bad", -100), ("Bad", -100)]
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


# phone_age_on_network_trigger_score



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



# @pytest.mark.parametrize(
#     "input_value, expected",
#     [
#         (None, 0),
#         ("saad.shaikh@datasutram.com", 0),
#         ("saad.shaikh123@datasutram.com", 0),
#         ("saad.shaikh123456@datasutram.com", -40),
#         ("", 0),
#     ],
# )
# def test_numbers_in_email_trigger_score(input_value, expected):
#     rule = {}
#     rule["base_score"] = 450
#     rule["numbers_in_email_trigger_score"] = rule_dict["numbers_in_email_trigger_score"]
#     score = get_score({"input_email": input_value}, rule)
#     assert score["ruleResponse"]["numbers_in_email_trigger_score"]["score"] == expected


# @pytest.mark.parametrize(
#     "input_value, expected",
#     [
#         (None, 0),
#         ("saad.shaikh@datasutram.com", 0),
#         ("saad.shaikh123@datasutram.com", 0),
#         ("saad.shaikh123656@datasutram.com", "Dubious Email"),
#         ("", 0),
#     ],
# )
# def test_email_num_count_tag(input_value, expected):
#     rule = {}
#     rule["base_score"] = 450
#     rule["email_num_count_tag"] = rule_dict["email_num_count_tag"]
#     score = get_score({"input_email": input_value}, rule)
#     print(score)
#     if score["tags"]:
#         assert score["tags"][0] == expected
#     else:
#         assert 0 == expected


# @pytest.mark.parametrize(
#     "input_value, expected",
#     [
#         ([0, 0], "Not Present on Whatsapp and Other relavant digital Platforms"),
#         ([1, 0], 0),
#         ([0, 1], 0),
#         ([None, None], 0),
#     ],
# )
# def test_flipkart_whatsapp_tag(input_value, expected):
#     rule = {}
#     rule["base_score"] = 450
#     rule["flipkart_whatsapp_tag"] = rule_dict["flipkart_whatsapp_tag"]
#     score = get_score(
#         {
#             "flipkart": input_value[0],
#             "whatsapp": input_value[1],
#         },
#         rule,
#     )
#     print(score)
#     if score["tags"]:
#         assert score["tags"][0] == expected
#     else:
#         assert 0 == expected


# @pytest.mark.parametrize(
#     "input_value, expected",
#     [(0, "PAN not Registered on ITR"), (1, 0), (None, "PAN not Registered on ITR")],
# )
# def test_tax_payer_tag(input_value, expected):
#     rule = {}
#     rule["base_score"] = 450
#     rule["tax_payer_tag"] = rule_dict["tax_payer_tag"]
#     score = get_score({"tax": input_value}, rule)
#     print(score)
#     if score["tags"]:
#         assert score["tags"][0] == expected
#     else:
#         assert 0 == expected


# @pytest.mark.parametrize(
#     "input_value, expected",
#     [
#         ("2018-01-01", 0),
#         ("2024-09-01", "Phone Picked up less than 6 Months"),
#         ("2024-01-01", "Phone Picked up less than 1 Year"),
#         ("2023-11-01", "Phone Picked up less than 1 Year"),
#     ],
# )
# def test_phonename_first_seen_tag(input_value, expected):
#     rule = {}
#     rule["base_score"] = 450
#     rule["phonename_first_seen_tag"] = rule_dict["phonename_first_seen_tag"]
#     score = get_score({"phone_name_first_seen_year": input_value}, rule)
#     print(score)
#     if score["tags"]:
#         assert score["tags"][0] == expected
#     else:
#         assert 0 == expected