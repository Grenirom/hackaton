import json
from decimal import Decimal

def search_object(function_):
    def wrapper(*args, **kwargs):
        self = args[0]
        id = args[1]
        for obj in self.objects:
            if obj['id'] == id:
                kwargs.update(object_=obj)
                return function_(*args, **kwargs)
        kwargs.update(object_=None)
        return function_(*args, **kwargs)
    return wrapper




class CreateMixin:         #работает
    def _get_or_set_objects_and_id(self):
        try:
            self.id
            self.objects
        except (NameError, AttributeError):
            self.objects = []
            self.id = 0
    
    def __init__(self) -> None:
        self._get_or_set_objects_and_id()

    def post(self, **kwargs):
        self.id += 1
        obj = dict(id=self.id, **kwargs)
        self.objects.append(obj)
        return f'Successfully Created! {obj}'
    
class ListingMixin:#работает
    def list(self):
        res = [{'id': obj['id'], 'brand': obj['brand'], 'model': obj['model'], 'year': obj['year'], 'engine': obj['engine'], 'color': obj['color'], 'body_type': obj['body_type'], 'mileage': obj['mileage'], 'price': obj['price']} for obj in self.objects]
        return f'Here you go! {res}'
    
    
        
class RetrieveMixin:     #Работает
    @search_object
    def get_one(self, id, **kwargs):
        obj = kwargs['object_']
        if obj:
            return {'msg': obj}
        else:
            return 'Haven\'t found!'


class UpdateMixin:   #Работает

    @search_object
    def update_one(self, id, **kwargs):
        obj = kwargs.pop('object_')
        if obj:
            obj.update(**kwargs)
            return {'Car': obj}
        return 'No such ID!'     
    
class DeleteMixin:  #Работает
    @search_object
    def delete(self, id, **kwargs):
        obj = kwargs['object_']
        if obj:
            self.objects.remove(obj)
            return 'Deleted!'
        return 'No such ID!'
    


class Cars(CreateMixin, ListingMixin, RetrieveMixin, UpdateMixin, DeleteMixin): 
    def add_to_json(self): #Работает
        with open('cars.json', 'w') as file:
            json.dump(self.objects, file, indent=4)
            print('Successfully saved info!')


car1 = Cars()
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='white', body_type='SUV', mileage=10000, price=150000))
print(car1.post(brand='Toyota', model='Corolla', year=2012, engine=3.5, color='Black', body_type='SUV', mileage=10000, price=150000))
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='green', body_type='SUV', mileage=10001230, price=90000))
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='golden', body_type='SUV', mileage=10000, price=15000))
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='purple', body_type='SUV', mileage=10000, price=12000))
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='WHITE', body_type='SUV', mileage=10000, price=120000))
print(car1.post(brand='BMW', model='X5', year=2022, engine=3.5, color='WHITE', body_type='SUV', mileage=10001230, price=150000))   

print(car1.list())
print(car1.get_one(5))
print(car1.update_one(1, brand='Ferrari', model='sf90'))
print(car1.delete(1))
