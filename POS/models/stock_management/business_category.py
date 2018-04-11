from sqlalchemy import Column, Integer

from POS.models.base_model import AppDB


class BusinessCategory(AppDB.BaseModel):
    """
        Link model for the business and category model
    """
    __tablename__ = "business_category"

    business_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, primary_key=True)

    def __init__(self, business_id, category_id):
        self.business_id = business_id
        self.category_id = category_id

    def __repr__(self):
        return "BusinessCategory<business_id={0}, category_id={1}>".format(
            self.business_id,
            self.category_id
        )
