import warnings

warnings.filterwarnings("ignore")


class LARSONTUBRO_1_0_0:
    def __init__(self):
        self.rules = self.get_rules()

    @staticmethod
    def get_rules():
        rule_dict = {
            "di_phonedi_combined_trigger_score": {
                ("digital_identity_score", "phone_name_d_i_score"): {},
                "digital_identity_score": {},
                "phone_name_d_i_score": {},
                "default_score": {},
            },
            "email_first_seen_year_trigger_score": {
                "email_first_seen_year": {},
                "email_first_seen_year_month_vintage": {},
            },
            "phone_email_first_seen_year_trigger_score": {
                "phone_email_first_seen_year": {},
                "phone_email_first_seen_year_month_vintage": {},
            },
            "phone_name_first_seen_year_trigger_score": {
                "phone_name_first_seen_year": {},
                "phone_name_first_seen_year_month_vintage": {},
            },
            "has_flipkart_trigger_score": {
                "flipkart": {}
            },
            "is_whatsapp_flipkart_absent_trigger_score": {
                "flipkart": {},
                "whatsapp": {},
                ("whatsapp", "flipkart"): {},
            },
            "is_whatsapp_available_trigger_score": {
                "whatsapp": {}
            },
            "is_tax_payer_trigger_score": {
                "tax": {}
            },
            "is_whatsapp_business_available_trigger_score": {
                "is_w_a_business": {}
            },
            "is_postpaid_phone_trigger_score": {
                "number_billing_type": {}
            },
            "vpa_available_trigger_score": {
                "vpa_available": {}
            },
            "vpa_name_match_trigger_score": {
                "vpa_available": {},
                "phone_vpa_name": {},
                "input_name": {},
                "similarity_class": {},
            },
            "has_multiple_email_with_phone_trigger_score": {
                "email_mapped_with_phone": {}
            },
            "risky_fintech_ratio_trigger_score": {
                "risky_fintech_count": {}
            },
            "is_ugly_bad_trigger_score": {
                "bad_ugly_match_found": {}
            },
            "is_demat_trigger_score" :{
                "is_demat_available":{}
            },
            "uan_available_trigger_score": {
                "uan_available": {}  
            }

            
        }

        true_vals = [1.0, 1, True, "1", "1.0", "True", "postpaid"]
        false_vals = [0.0, 0, False, "0", "0.0", "False"]
        ugly_vals = ["ugly", "Ugly"]
        bad_vals = ["bad", "Bad"]


        rule_dict["di_phonedi_combined_trigger_score"][
            ("digital_identity_score", "phone_name_d_i_score")
        ]["sequential_triggers"] = [True]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "null_check"
        ] = [[0]]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "<="
        ] = [[200, 0]]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "between_1"
        ] = [
            [[200, 400], 20],
            [[400, 600], 50],
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            ">"
        ] = [[600, 80]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][
            "null_check"
        ] = [[0]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"]["<="] = [
            [200, -40]
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][
            "between_1"
        ] = [[[200, 400], 20], [[400, 600], 50]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][">"] = [
            [600, 80]
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["default_score"][
            "get_default_score"
        ] = [-70]


        #email_first_seen_year_trigger_score
        rule_dict["email_first_seen_year_trigger_score"]["email_first_seen_year"][
            "null_check"
        ] = [[0]]
        rule_dict["email_first_seen_year_trigger_score"]["email_first_seen_year"][
            "empty_string_check"
        ] = [[0]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["time_in_yrs"] = [["email_first_seen_year"]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["=="] = [[[0], -40, {'email_vintage_1_tag':'di16'}], [[1], 0,{'email_vintage_1_tag':'di16'}], [[2, 3], 10], [[4, 5], 20]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["between_1"] = [[[5, 10], 30]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ][">"] = [[10, 40]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["else"] = [0]


        #phone_email_first_seen_year_trigger_score
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year"
        ]["null_check"] = [[0]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year"
        ]["empty_string_check"] = [[0]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["time_in_yrs"] = [["phone_email_first_seen_year"]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["=="] = [[[0], -40], [[1], 0], [[2, 3], 10], [[4, 5], 20]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["between_1"] = [[[5, 10], 30]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ][">"] = [[10, 40]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["else"] = [0]


        #phone_name_first_seen_year_trigger_score
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year"
        ]["null_check"] = [[0]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year"
        ]["empty_string_check"] = [[0]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["time_in_yrs"] = [["phone_name_first_seen_year"]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["=="] = [[[0], -40], [[1], 0], [[2, 3], 10], [[4, 5], 20]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["between_1"] = [[[5, 10], 30]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ][">"] = [[10, 40]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["else"] = [0]

        #has_flipkart_trigger_score
        rule_dict["has_flipkart_trigger_score"]["flipkart"]["null_check"] = [[0]]
        rule_dict["has_flipkart_trigger_score"]["flipkart"]["=="] = [
            [false_vals, -30,{'flipkart_absent_tag':"df03"}],
            [true_vals, 0],
        ]
        rule_dict["has_flipkart_trigger_score"]["flipkart"]["else"] = [0]

        #is_whatsapp_flipkart_absent_trigger_score
        rule_dict["is_whatsapp_flipkart_absent_trigger_score"]["flipkart"][
            "null_check"
        ] = [[0]]
        rule_dict["is_whatsapp_flipkart_absent_trigger_score"]["whatsapp"][
            "null_check"
        ] = [[0]]
        rule_dict["is_whatsapp_flipkart_absent_trigger_score"][
            ("whatsapp", "flipkart")
        ]["x_and_y"] = [
            [false_vals, false_vals, -150],
            [false_vals, true_vals, 0],
            [true_vals, false_vals, 0],
            [true_vals, true_vals, 0],
        ]
        rule_dict["is_whatsapp_flipkart_absent_trigger_score"][
            ("whatsapp", "flipkart")
        ]["else"] = [0]


        #is_whatsapp_available_trigger_score
        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["null_check"] = [
            [0]
        ]
        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["=="] = [
            [false_vals, -100,{"whatsapp_absent_tag":"df02"}],
            [true_vals, 0],
        ]
        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["else"] = [0]

        #is_tax_payer_trigger_score
        rule_dict["is_tax_payer_trigger_score"]["tax"]["null_check"] = [[0]]
        rule_dict["is_tax_payer_trigger_score"]["tax"]["=="] = [
            [true_vals, 70],
            [false_vals, -50,{"tax_absent_tag":"df05"}],
        ]
        rule_dict["is_tax_payer_trigger_score"]["tax"]["else"] = [0]


        ##cdsl trigger missing ------------------------------------------------------------------------
        #is_demat_trigger_score
        rule_dict['is_demat_trigger_score']["is_demat_available"]['null_check']= [[0]]
        rule_dict["is_demat_trigger_score"]["is_demat_available"]["=="] = [[true_vals,20],[false_vals,0]]
        rule_dict['is_demat_trigger_score']["is_demat_available"]['else'] = [0]

        #is_whatsapp_business_available_trigger_score
        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "null_check"
        ] = [[0]]
        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "=="
        ] = [[true_vals, 10], [false_vals, 0]]
        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "else"
        ] = [0]
        
        #is_postpaid_phone_trigger_score
        rule_dict["is_postpaid_phone_trigger_score"]["number_billing_type"][
            "null_check"
        ] = [[0]]
        rule_dict["is_postpaid_phone_trigger_score"]["number_billing_type"]["=="] = [
            [true_vals, 150],
            [false_vals, 0],
        ]
        rule_dict["is_postpaid_phone_trigger_score"]["number_billing_type"]["else"] = [
            0
        ]

        #vpa_available_trigger_score
        rule_dict["vpa_available_trigger_score"]["vpa_available"]["null_check"] = [[0]]
        rule_dict["vpa_available_trigger_score"]["vpa_available"]["=="] = [
            [false_vals, -20, {"vpa_absent_tag":"df04"}],
            [true_vals, 50],
        ]
        rule_dict["vpa_available_trigger_score"]["vpa_available"]["else"] = [0]


        #vpa_name_match_trigger_score
        rule_dict["vpa_name_match_trigger_score"]["vpa_available"]["null_check"] = [[0]]
        rule_dict["vpa_name_match_trigger_score"]["vpa_available"]["=="] = [
            [false_vals, 0]
        ]
        rule_dict["vpa_name_match_trigger_score"]["phone_vpa_name"]["null_check"] = [
            [0]
        ]
        rule_dict["vpa_name_match_trigger_score"]["input_name"]["null_check"] = [[0]]
        rule_dict["vpa_name_match_trigger_score"]["similarity_class"][
            "get_similarity_class"
        ] = [["input_name", "phone_vpa_name"]]
        rule_dict["vpa_name_match_trigger_score"]["similarity_class"]["=="] = [
            [["0"], 0],
            [["1"], -20,{"vpa_name_match1_tag":"nm01"}],
            [["2"], 10,{"vpa_name_match2_tag":"nm05"}],
            [["3"], 30],
        ]
        rule_dict["vpa_name_match_trigger_score"]["similarity_class"]["else"] = [0]


        #has_multiple_email_with_phone_trigger_score
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["null_check"] = [[0]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ][">"] = [[6, -50,{"email_mapped_with_phone_tag":"mi01"}]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["<="] = [[6, 0]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["else"] = [0]        
        

        #is_uan_presenet_trigger_score ----------------------------------------------------------------------------------------
        rule_dict["uan_available_trigger_score"]["uan_available"]["null_check"] = [[0]]
        rule_dict["uan_available_trigger_score"]["uan_available"]["=="] = [[true_vals, 30],[false_vals, 0]]
        rule_dict["uan_available_trigger_score"]["uan_available"]["else"] = [0]


        rule_dict["risky_fintech_ratio_trigger_score"]["risky_fintech_count"][
            "null_check"
        ] = [[0]]
        rule_dict["risky_fintech_ratio_trigger_score"]["risky_fintech_count"][">"] = [
            [0, -50, {"risky_fintech_tag":"df07"}]
        ]
        rule_dict["risky_fintech_ratio_trigger_score"]["risky_fintech_count"]["=="] = [
            [[0], 0]
        ]
        rule_dict["risky_fintech_ratio_trigger_score"]["risky_fintech_count"][
            "else"
        ] = [0]
        

        rule_dict["is_ugly_bad_trigger_score"]["bad_ugly_match_found"]["null_check"] = [
            [0]
        ]
        rule_dict["is_ugly_bad_trigger_score"]["bad_ugly_match_found"]["=="] = [
            [bad_vals, -100],
            [ugly_vals, -300],
        ]
        rule_dict["is_ugly_bad_trigger_score"]["bad_ugly_match_found"]["else"] = [0]


        #important please check ------------------------------------------------------------------------
        rule_dict["base_score"] = 450

        return rule_dict