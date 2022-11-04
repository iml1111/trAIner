from trainer import Trainer
from fasttext import Recommender
from data_loader import data_loader

print("Train Data Loading...")
train_data = data_loader()

trainer = Trainer() 
trainer.set_params(
    vec_size=31,
    windows=10,
    min_count=30,
    iteration=1200,
    workers=16
)

trainer.set_corpora(train_data) 
trainer.train()
trainer.save_model(path="./signus_ft_model_v1")

recommender = Recommender("./signus_ft_model_v1")
recommender.make_test_report()