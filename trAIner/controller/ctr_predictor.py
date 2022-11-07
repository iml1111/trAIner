import numpy as np
from controller.exceptions import (
	UserIndexError, ItemIndexError
)

class CTRPredictor:

	def __init__(self, ctr_model_path: str):
		self.ctr_model_path = ctr_model_path
		self.pred_matrix = np.load(ctr_model_path)

	def predict(self, user_id: int, item_id: int):
		y_pred = self.predict_probe(user_id, item_id)
		y_pred = True if y_pred >= 3 else False
		return y_pred

	def predict_probe(self, user_id: int, item_id: int):

		if not (0 <= user_id <= 1002):
			raise UserIndexError()
		if not (0 <= item_id <= 1187):
			raise ItemIndexError()

		y_pred = self.pred_matrix[item_id, user_id]
		return y_pred


if __name__ == '__main__':
	from config import config

	predictor = CTRPredictor(config.CTR_MODEL_PATH)

	# Normal Case
	user_id, item_id = 569, 586
	print(
		f"User({user_id})의 Item({item_id})의 클릭 여부:", 
		predictor.predict(user_id, item_id)
	)
	# 3보다 높으면 True, 낮으면 False
	print(
		f"User({user_id})의 Item({item_id})의 Probe Value:", 
		predictor.predict_probe(user_id, item_id)
	)

	# Error Case
	try:
		user_id, item_id = 99999, 0
		predictor.predict(user_id, item_id)
	except UserIndexError:
		print("UserIndexError 발생.")
	
	try:
		user_id, item_id = 0, 99999
		predictor.predict(user_id, item_id)
	except ItemIndexError:
		print("ItemIndexError 발생.")



