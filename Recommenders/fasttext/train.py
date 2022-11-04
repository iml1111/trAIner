from trainer import Trainer
from recommender import Recommender
from data_loader import load_corpora

print("Train Data Loading...")
train_data = load_corpora()

trainer = Trainer() 
trainer.set_params(
    vec_size=30,
    windows=10,
    min_count=5,
    iteration=100,
    workers=3
)

trainer.set_corpora(train_data) 
trainer.train()
trainer.save_model(path="./ft_model_v1")

recommender = Recommender("./ft_model_v1")
recommender.make_test_report()