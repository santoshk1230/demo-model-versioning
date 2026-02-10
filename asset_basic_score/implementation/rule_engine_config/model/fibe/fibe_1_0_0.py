import warnings

warnings.filterwarnings("ignore")

class FIBE_1_0_0:
    def __init__(self):
        self.rules = self.get_rules()

    @staticmethod
    def get_rules():
        rule_dict = {
            "cdsl_trigger_score": {
                "cdsl": {}
            },
            "indexed_name_match_trigger_score": { 
                "indexed_name_match_score": {},
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

            "is_whatsapp_available_trigger_score": {"whatsapp": {}}, 

            "is_tax_payer_trigger_score": {"tax": {}},

            "is_whatsapp_business_available_trigger_score": {"is_w_a_business": {}}, 

            "is_postpaid_phone_trigger_score": {"number_billing_type": {}}, 

            "phone_age_on_network_trigger_score": { 
                "date_aon": {},
                "date_aon_month": {},
            },
            "vpa_available_trigger_score": {"vpa_available": {}}, 
            "vpa_name_match_trigger_score": { 
                "vpa_available": {},
                "phone_vpa_name": {},
                "input_name": {},
                "similarity_class": {},
            },
            "has_multiple_email_with_phone_trigger_score": { 
                "email_mapped_with_phone": {}
            },
            "di_phonedi_combined_trigger_score": { 
                ("digital_identity_score", "phone_name_d_i_score"): {},
                "digital_identity_score": {},
                "phone_name_d_i_score": {},
                "default_score": {},
            },
            "is_pan_email_present_trigger_score": {"pan_email_present": {}}, 
            "inactive_gst_trigger_score" : {"inactive_gst_count":{}},
        }
        
        true_vals = [1.0, 1, True, "1", "1.0", "True", "postpaid", "Postpaid"]
        false_vals = [0.0, 0, False, "0", "0.0", "False", "prepaid", "Prepaid"]
        ugly_vals = ["ugly", "Ugly"]
        bad_vals = ["bad", "Bad"]

        rule_dict["cdsl_trigger_score"]["cdsl"]["null_check"] = [[0]]
        rule_dict["cdsl_trigger_score"]["cdsl"]["=="] = [[true_vals, 20],[false_vals, 0]]
        rule_dict["cdsl_trigger_score"]["cdsl"]["else"] = [0]

        rule_dict["indexed_name_match_trigger_score"]["indexed_name_match_score"][
            "null_check"
        ] = [[0]]
        rule_dict["indexed_name_match_trigger_score"]["indexed_name_match_score"][
            "empty_string_check"
        ] = [[0]]
        rule_dict["indexed_name_match_trigger_score"]["indexed_name_match_score"][
            "between_1"
        ]=[[[0,5],-50],
           [[5,40],0],
           [[40,60],10],
           [[60,80],20], 
           [[80,100],30]
           ]
        rule_dict['indexed_name_match_trigger_score']["indexed_name_match_score"]["else"]=[0]

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
        ]["=="] = [[[1], -40], [[2], 0], [[4], 10], [[6], 20]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["between_1"] = [[[7, 13], 30]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ][">"] = [[13, 40]]
        rule_dict["email_first_seen_year_trigger_score"][
            "email_first_seen_year_month_vintage"
        ]["else"] = [0]


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
        ]["=="] = [[[1], -40], [[2], 0], [[4], 10], [[6], 20]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["between_1"] = [[[7, 13], 30]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ][">"] = [[13, 40]]
        rule_dict["phone_email_first_seen_year_trigger_score"][
            "phone_email_first_seen_year_month_vintage"
        ]["else"] = [0]
        

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
        ]["=="] = [[[1], -40], [[2], 0], [[4], 10], [[6], 20]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["between_1"] = [[[7, 13], 30]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ][">"] = [[13, 40]]
        rule_dict["phone_name_first_seen_year_trigger_score"][
            "phone_name_first_seen_year_month_vintage"
        ]["else"] = [0]

        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["null_check"] = [
            [0]
        ]
        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["=="] = [
            [false_vals, -100],
            [true_vals, 0],
        ]
        rule_dict["is_whatsapp_available_trigger_score"]["whatsapp"]["else"] = [0]

        rule_dict["is_tax_payer_trigger_score"]["tax"]["null_check"] = [[0]]
        rule_dict["is_tax_payer_trigger_score"]["tax"]["=="] = [
            [true_vals, 70],
            [false_vals, -50],
        ]
        rule_dict["is_tax_payer_trigger_score"]["tax"]["else"] = [0]

        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "null_check"
        ] = [[0]]
        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "=="
        ] = [[true_vals, 10], [false_vals, 0]]
        rule_dict["is_whatsapp_business_available_trigger_score"]["is_w_a_business"][
            "else"
        ] = [0]


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

        rule_dict["phone_age_on_network_trigger_score"]["date_aon"]["null_check"] = [
            [0]
        ]
        rule_dict["phone_age_on_network_trigger_score"]["date_aon_month"][
            "time_in_months"
        ] = [["date_aon"]]
        rule_dict["phone_age_on_network_trigger_score"]["date_aon_month"]["<"] = [
            [12, -60]
        ]
        rule_dict["phone_age_on_network_trigger_score"]["date_aon_month"][
            "between_1"
        ] = [[[0, 18], -60], [[18, 30], -40], [[29, 42], 0], [[42, 78], 50]]
        rule_dict["phone_age_on_network_trigger_score"]["date_aon_month"][">"] = [
            [78, 100]
        ]
        rule_dict["phone_age_on_network_trigger_score"]["date_aon_month"]["else"] = [0]

        rule_dict["vpa_available_trigger_score"]["vpa_available"]["null_check"] = [[0]]
        rule_dict["vpa_available_trigger_score"]["vpa_available"]["=="] = [
            [false_vals, -20],
            [true_vals, 50],
        ]
        rule_dict["vpa_available_trigger_score"]["vpa_available"]["else"] = [0]


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
            [["1"], -20],
            [["2"], 10],
            [["3"], 30],
        ]
        rule_dict["vpa_name_match_trigger_score"]["similarity_class"]["else"] = [0]

        
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["null_check"] = [[0]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["=="]=[[[0],0]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["between_1"] = [[[0, 3],0],[[3,6],0]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ][">"] =[[6,-50]]
        rule_dict["has_multiple_email_with_phone_trigger_score"][
            "email_mapped_with_phone"
        ]["else"] = [0]


        rule_dict["di_phonedi_combined_trigger_score"][
            ("digital_identity_score", "phone_name_d_i_score")
        ]["sequential_triggers"] = [True]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "null_check"
        ] = [[0]]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "<="
        ] = [[300, -30]]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            "between_1"
        ] = [
            [[300, 600], -30]
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["digital_identity_score"][
            ">"
        ] = [[600, 10]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][
            "null_check"
        ] = [[0]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"]["<="] = [
            [300, -30]
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][
            "between_1"
        ] = [[[300, 600], -30]]
        rule_dict["di_phonedi_combined_trigger_score"]["phone_name_d_i_score"][">"] = [
            [600, 10]
        ]
        rule_dict["di_phonedi_combined_trigger_score"]["default_score"][
            "get_default_score"
        ] = [0]

        rule_dict["is_pan_email_present_trigger_score"]["pan_email_present"][
            "null_check"
        ] = [[0]]
        rule_dict["is_pan_email_present_trigger_score"]["pan_email_present"]["=="] = [
            [false_vals, -10],
            [true_vals, 10],
        ]
        rule_dict["is_pan_email_present_trigger_score"]["pan_email_present"]["else"] = [
            0
        ]

        rule_dict["inactive_gst_trigger_score"]["inactive_gst_count"]["null_check"] = [[0]]
        rule_dict["inactive_gst_trigger_score"]["inactive_gst_count"]["=="]=[[[0],0],[[1],-20],[[2],-40],[[3],-60],[[4],-80]]
        rule_dict["inactive_gst_trigger_score"]["inactive_gst_count"][">="] = [[5,-100]]
        rule_dict['inactive_gst_trigger_score']["inactive_gst_count"]['else'] =  [0]

        rule_dict["base_score"] = 450


        return rule_dict