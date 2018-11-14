from wine import db
class wine(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    winename=db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return f"wine('{self.winename}')"