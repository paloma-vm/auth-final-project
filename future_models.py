class Menu(db.Model):
    """Menu model"""
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    breakfast = db.Column(db.String(80), nullable=False)
    lunch = db.Column(db.String(80), nullable=False)
    dinner = db.Column(db.String(80), nullable=False)
    snacks = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Menu: '{self.date}'"
    

# class Medication(db.Model):
#     """Medication model"""
#     __tablename__ = 'medications'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     dosage = db.Column(db.String(80), nullable=False)
#     frequency = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return f"Medication: '{self.name}"
    
    # client_medication_table = db.Table('client_medications',
#     db.Column('client_id', db.Integer, db.ForeignKey('clients.id'), primary_key=True),
#     db.Column('medication_id', db.Integer, db.ForeignKey('medications.id'), primary_key=True)
# )

# previous model, not needed because family and caregiver are both users
# class Caregiver(db.Model):
#     """Caregiver model"""
#     __tablename__ = 'caregivers'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     address = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     clients_under_care = db.relationship('Client', secondary='caregivers_clients', back_populates='caregiver', lazy=True)

#     def __repr__(self):
#         return f"Caregiver: '{self.name}'"