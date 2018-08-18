import pandas as pd
import pickle
import numpy as np
import sklearn
import gib_detect_train
import datetime
from sklearn.ensemble import GradientBoostingClassifier

class Preprocessor:

	@staticmethod
	def preprocess(obj):
		pdf = pd.DataFrame(obj,index=[0])
		pdf = Preprocessor.apply_name_filters(pdf)
		pdf = Preprocessor.apply_date_filters(pdf)
		pdf = Preprocessor.apply_trans_filters(pdf)
		pdf = Preprocessor.factorize_cat_cols(pdf)
		pdf = Preprocessor.remove_unused_features(pdf)
		pdf = Preprocessor.reorder_cols(pdf)
		return pdf.values

	@staticmethod
	def vowel_ratio(x):
	    count = 0
	    for c in x.lower():
	        if c in ['a', 'e', 'i', 'o', 'u']:
	            count=count+1
	    return float(count)/float(len(x))

	@staticmethod
	def apply_name_filters(pdf):
	    # name length
	    pdf['name_len'] = pdf['name'].map(lambda x : len(x))
	    
	    # name gibberish score
	    name_model_data = pickle.load(open('../private/gib_model.pki', 'rb'))
	    name_model_mat = name_model_data['mat']
	    gib_score = lambda x : gib_detect_train.avg_transition_prob(x, name_model_mat)
	    pdf['name_gibberish_score'] = pdf['name'].map(gib_score)
	    
	    # name vowel ratio
	    pdf['name_vowel_ratio'] = pdf['name'].apply(Preprocessor.vowel_ratio)
	    
	    return pdf

	@staticmethod
	def get_day_of_week(x):
	    date_str = x[:10]
	    datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
	    return datetime_obj.weekday()

	@staticmethod
	def get_time_of_day(x):
	    time_str = x[-8:-6] + x[-5:-3]
	    return int(time_str)

	@staticmethod
	def apply_date_filters(pdf):
	    # get day of week
	    pdf['day_of_week'] = pdf['receive_date'].apply(Preprocessor.get_day_of_week)
	    
	    # get time of day
	    pdf['time_of_day'] = pdf['receive_date'].apply(Preprocessor.get_time_of_day)
	    
	    return pdf

	@staticmethod
	def is_nan(x):
	    return int(np.isnan(x))

	@staticmethod
	def impute_filter_values(x):
	    if np.isnan(x):
	        return 0
	    else:
	        return x

	@staticmethod
	def apply_trans_filters(pdf):
	    # check isnan
	    pdf['utm_filter_isnan'] = pdf['utm_filter'].apply(Preprocessor.is_nan)
	    pdf['avs_filter_isnan'] = pdf['avs_filter'].apply(Preprocessor.is_nan)
	    pdf['email_domain_filter_isnan'] = pdf['email_domain_filter'].apply(Preprocessor.is_nan)
	    pdf['ip_filter_isnan'] = pdf['ip_filter'].apply(Preprocessor.is_nan)
	    pdf['cvv_filter_isnan'] = pdf['cvv_filter'].apply(Preprocessor.is_nan)
	    pdf['country_filter_isnan'] = pdf['country_filter'].apply(Preprocessor.is_nan)
	    pdf['minfraud_filter_isnan'] = pdf['minfraud_filter'].apply(Preprocessor.is_nan)
	    
	    # impute values if isnan
	    pdf['utm_filter'] = pdf['utm_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['avs_filter'] = pdf['avs_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['email_domain_filter'] = pdf['email_domain_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['ip_filter'] = pdf['ip_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['cvv_filter'] = pdf['cvv_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['country_filter'] = pdf['country_filter'].apply(Preprocessor.impute_filter_values)
	    pdf['minfraud_filter'] = pdf['minfraud_filter'].apply(Preprocessor.impute_filter_values)
	    
	    return pdf

	@staticmethod
	def factorize_cat_cols(pdf):
		mapping = pd.read_pickle('../private/data-mappings.pkl')

		# factorize using training data-mappings
		pdf['country'] = np.where(mapping['country'].values==pdf['country'].values[0])[0][0]
		pdf['currency'] = np.where(mapping['currency'].values==pdf['currency'].values[0])[0][0]
		pdf['financial_type_id'] = np.where(mapping['financial_type_id'].values==pdf['financial_type_id'].values[0])[0][0]
		pdf['gateway'] = np.where(mapping['gateway'].values==pdf['gateway'].values[0])[0][0]
		pdf['payment_instrument_id'] = np.where(mapping['payment_instrument_id'].values==pdf['payment_instrument_id'].values[0])[0][0]
		pdf['payment_method'] = np.where(mapping['payment_method'].values==pdf['payment_method'].values[0])[0][0]
		pdf['utm_campaign'] = np.where(mapping['utm_campaign'].values==pdf['utm_campaign'].values[0])[0][0]
		pdf['utm_medium'] = np.where(mapping['utm_medium'].values==pdf['utm_medium'].values[0])[0][0]

		return pdf

	@staticmethod
	def remove_unused_features(pdf):
	    pdf = pdf.drop(['name', 'receive_date', 'contrib_id'], axis=1)
	    return pdf

	@staticmethod
	def reorder_cols(pdf):
	    pdf = pdf[['financial_type_id','payment_instrument_id','usd_amount','currency','total_amount','gateway','payment_method','country','utm_medium','utm_campaign','avs_filter','cvv_filter','country_filter','email_domain_filter','utm_filter','ip_filter','minfraud_filter','name_len','name_gibberish_score','name_vowel_ratio','day_of_week','time_of_day','utm_filter_isnan','avs_filter_isnan','email_domain_filter_isnan','ip_filter_isnan','cvv_filter_isnan','country_filter_isnan','minfraud_filter_isnan']]
	    return pdf
