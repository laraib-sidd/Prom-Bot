from db.functions import lists, db_func
import random

data = {"user_id": [], "name": [], "age": [],
        "city": [], "phone": [], "region": [], "promo_code": [],
        "referral": [], "referral_points": []}


def check_referal(code):
    if code in lists.promo_list:
        id = lists.user_list[lists.promo_list.index(code)]
        db_func.update_referral(id)
        data['referral'] = 0
        data['referral_points'] = 0
        return True

    else:
        data['referral'] = 0
        data['referral_points'] = 0
        return False


def get_promo_code():

    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, 8):

        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    if code in lists.promo_list:
        return get_promo_code()
    else:
        return code
