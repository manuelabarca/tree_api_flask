from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('person.id'))


    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
            # do not serialize the password, its a security breach
        }

    def create(name, last_name, rol, age, father_id, mother_id):
        person = Person(name=name, last_name=last_name, rol=rol, age=age, father_id=father_id, mother_id=mother_id)
        db.session.add(person)
        db.session.commit()
    
    def getAll():
        people = Person.query.order_by(Person.age.desc())
        people = list(map(lambda person: person.serialize(), people))
        return people
    
    def get_member_by_id(id):
        Me = Person.query.get(id)
        Dad = Person.query.filter_by(id=Me.father_id).first()
        if Dad is None:
            Dad = ""
        Mom = Person.query.filter_by(id=Me.mother_id).first()
        if Mom is None:
            Mom = ""
        Son = Person.query.filter( (Person.father_id == id) | (Person.mother_id == id) ).first()
        if Son is None:
            Son = []
        family = {
            "dad": Person.serialize(Dad),
            "mom": Person.serialize(Mom),
            "me": Person.serialize(Me),
            "son": Person.serialize(Son)
        }
        return family