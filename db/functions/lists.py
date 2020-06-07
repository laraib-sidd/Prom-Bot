from db.functions import db_func

# DataRetrived from database
user_list = db_func.search("user_id")
promo_list = db_func.search("PromoCode")
referral_list = db_func.search("Referral")
referral_point_list = db_func.search("Referral_Points")
name_list = db_func.search("Name")
age_list = db_func.search("Age")
city_list = db_func.search("City")
region_list = db_func.search("Region")
phone_list = db_func.search("Phone")
