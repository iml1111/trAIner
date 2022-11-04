from modules.recommender.fasttext import Recommender

recommender = Recommender("./ft/soojle_ft_model")

print(recommender.doc2words("python"))
recommender.make_test_report()