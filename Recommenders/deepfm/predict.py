import os
import torch
from pprint import pprint
from model import DeepFactorizationMachineModel
from dotenv import load_dotenv

load_dotenv(verbose=True)
DEEP_MODEL_PATH = os.getenv('DEEP_MODEL_PATH')

model_data = torch.load(
	DEEP_MODEL_PATH,
	map_location=torch.device('cpu')
)
model_state_dict = model_data['model']
model_config = model_data['config']
# pprint(model_config)

# Users: 1003, Items: 1188 (1003, 1188)

model = DeepFactorizationMachineModel(
	[1003, 1188],
	model_config.embed_dim,
	model_config.mlp_dims,
	model_config.dropout,
).to('cpu')

model.load_state_dict(model_state_dict)

# UserId, ItemId
x = torch.tensor([[22,605]])
# print(x.size())

with torch.no_grad():
	model.eval()
	y = model(x)
	print(y)