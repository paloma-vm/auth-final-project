"""create db models to represent tables"""
from care_app.extensions import db
from sqlalchemy.orm import backref

class FormEnum(enum.Enum):
    """Helper class to use enums with forms"""
    @classmethod
    def choices(cls):
        return[(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Diet(FormEnum):
    NO_RESTRICTIONS = 'No Dietary Restrictions'
    DIABETIC = 'Diabetic'
    GLUTEN_FREE = 'Gluten Free'
    VEGETARIAN = 'Vegetarian'
    VEGAN = 'Vegan'
    LOW_SODIUM = 'Low Sodium'

