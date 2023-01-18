from mongoengine import Document,\
    StringField,\
    DateTimeField,\
    ObjectIdField,\
    BooleanField

from models.mongo_models.base_model import ToDictMixin


class Items(Document, ToDictMixin):
    """
    Таблица 1 thing:
    id,
    name: str,
    description: str,
    wrnt (гарантия/срок годности): datetime,
    master (создатель вещи, ее хозяин): ObjectID.
    work - вещь находится в работе
    public - вещь отображается у других пользователей (кроме админов)

    """
    name = StringField(required=True)
    description = StringField()
    wrnt = DateTimeField(required=True)
    master = ObjectIdField(required=False)
    work = BooleanField(required=False, default=False)
    public = BooleanField(required=False, default=False)
    meta = {
        'indexes': [
            'name', 'master'
        ]
    }
