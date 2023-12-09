
class ReviewDto:
    def __init__(self, score, username, review):
        self.score = score
        self.username = username
        self.review = review

    @property
    def score(self):
        return self.score

    @score.setter
    def score(self, score):
        self.score = score

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, username):
        self.username = username

    @property
    def review(self):
        return self.review

    @review.setter
    def review(self, review):
        self.review = review
