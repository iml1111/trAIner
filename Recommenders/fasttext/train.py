from trainer import Trainer
from recommender import Recommender
from data_loader import load_corpora

print("Train Data Loading...")
train_data = load_corpora()

trainer = Trainer() 
trainer.set_params(
    vec_size=30,
    windows=20,
    min_count=13,
    iteration=140,
    workers=3
)

trainer.set_corpora(train_data) 
trainer.train()
trainer.export_tsv()
trainer.save_model(path="./topic_model.w2v")

recommender = Recommender("./topic_model.w2v")
recommender.make_test_report()