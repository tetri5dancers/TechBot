import json
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer


class MLPModel():
    def __init__(self, intents):
        self.vectorizer = None
        self.mlp_model = None
        self.X = []
        self.Y = []
        self.INTENTS = intents
        self.training_result = None
        self.vectoriser_train()
        self.train()

    def vectoriser_train(self):
        """
        with open("train_collab.json", "r", encoding='utf-8') as config_file:
            BIG_INTENTS = json.load(config_file)

        self.INTENTS = BIG_INTENTS["intents"]
        """
        if self.INTENTS is None:
            return

        for name, intent in self.INTENTS.items():  # Для каждого интента
            for phrase in intent['examples']:  # Смотрим все фразы
                self.X.append(phrase.lower())  # Дописываем в списки
                self.Y.append(name)

            for phrase in intent['responses']:
                self.X.append(phrase)
                self.Y.append(name)

        self.vectorizer = CountVectorizer()
        self.vectorizer.fit(self.X)  # Обучаем векторайзер

    def train(self):
        if self.INTENTS is None:
            return

        self.mlp_model = MLPClassifier(solver="lbfgs", max_iter=250, verbose=False, tol=0.0002)
        # Создаем модель
        vecX = self.vectorizer.transform(self.X)  # Преобразуем тексты в вектора
        self.mlp_model.fit(vecX, self.Y)  # Обучаем модель
        self.training_result = self.mlp_model.score(vecX, self.Y)
        print(f"Model Ready: {self.training_result}")

    def get_intent_ml(self, text):
        vec_text = self.vectorizer.transform([text])
        intent = self.mlp_model.predict(vec_text)[0]
        return intent

    def vectorise(self, text):
        vec_text = self.vectorizer.transform([text])
        return vec_text

    def process(self, text):
        print(text, "-----", self.get_intent_ml(f"{text}"))

def main():
    mlpmodel = MLPModel()
    mlpmodel.process("Здравтсвуйте не могу зайти в здравницу")

if __name__ == '__main__':
    main()
