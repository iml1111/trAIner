from recommender import Recommender

recommender = Recommender("./ft_model_v1")

print(recommender.doc2words("987"))
print(recommender.doc_sim("982", "987"))
print(recommender.doc_sim("123", "897"))
print(recommender.is_in_dict("987"))
print(recommender.is_in_dict("987123123"))