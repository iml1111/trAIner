import numpy as np



class CTRPredictor:

	def __init__(self, model_path: str):
		self.pred_matrix = np.load(model_path)

	def predict(self, user_id: int, item_id: int):
		y_pred = self.pred_matrix[item_id, user_id]
		y_pred = True if y_pred >= 3 else False
		return y_pred

	def predict_probe(self, user_id: int, item_id: int):
		y_pred = self.pred_matrix[item_id, user_id]
		return y_pred


if __name__ == '__main__':
	predictor = CTRPredictor('./ctr_model.npy')
	user_id, item_id = 569,586
	
	print(predictor.predict(user_id, item_id))
	
	print(predictor.predict_probe(user_id, item_id))