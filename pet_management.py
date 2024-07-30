from abc import ABC, abstractmethod
import json


# Put all the class definitions here: Pet, Dog, Cat, Owner, PetManagementSystem
# This includes all the code from the first code block in my previous response
class Pet(ABC):
    total_pets = 0

    def __init__(self, name, species, age, owner, vaccinated=False):
        self.name = name
        self.species = species
        self.age = age
        self.owner = owner
        self.__vaccinated = vaccinated
        Pet.total_pets += 1

    def __str__(self):
        return f"{self.name} ({self.species}), Age: {self.age}, Owner: {self.owner.name}"

    def __eq__(self, other):
        if isinstance(other, Pet):
            return self.name == other.name and self.species == other.species
        return False

    def is_vaccinated(self):
        return self.__vaccinated

    def set_vaccinated(self, status):
        self.__vaccinated = status

    def mark_as_vaccinated(self):
        self.__vaccinated = True

    def human_age(self):
        return self.age * 7

    @classmethod
    def total_pets_count(cls):
        return cls.total_pets

    @abstractmethod
    def make_sound(self):
        pass


class Dog(Pet):
    def __init__(self, name, age, owner, breed, vaccinated=False):
        super().__init__(name, "Dog", age, owner, vaccinated)
        self.breed = breed

    def __str__(self):
        return f"{super().__str__()}, Breed: {self.breed}"

    def make_sound(self):
        return "Woof!"


class Cat(Pet):
    def __init__(self, name, age, owner, indoor, vaccinated=False):
        super().__init__(name, "Cat", age, owner, vaccinated)
        self.indoor = indoor

    def __str__(self):
        return f"{super().__str__()}, Indoor: {'Yes' if self.indoor else 'No'}"

    def make_sound(self):
        return "Meow!"


class Owner:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.pets = []

    def __str__(self):
        pet_names = ", ".join([pet.name for pet in self.pets])
        return f"{self.name} (Phone: {self.phone_number}), Pets: {pet_names}"

    def add_pet(self, pet):
        self.pets.append(pet)

    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)


class PetManagementSystem:
    def __init__(self):
        self.owners = []
        self.pets = []

    def add_owner(self, owner):
        self.owners.append(owner)

    def add_pet(self, pet):
        if pet.is_vaccinated():
            self.pets.append(pet)
            pet.owner.add_pet(pet)
        else:
            raise ValueError("Only vaccinated pets can be registered.")

    def get_all_owners(self):
        return self.owners

    def get_all_pets(self):
        return self.pets

    def save_to_file(self, filename='pet_management_data.json'):
        data = {
            'owners': [{'name': owner.name, 'phone_number': owner.phone_number} for owner in self.owners],
            'pets': [{'name': pet.name, 'species': pet.species, 'age': pet.age,
                      'owner': pet.owner.name, 'vaccinated': pet.is_vaccinated()} for pet in self.pets]
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self, filename='pet_management_data.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.owners = [Owner(owner['name'], owner['phone_number']) for owner in data['owners']]

            for pet_data in data['pets']:
                owner = next((owner for owner in self.owners if owner.name == pet_data['owner']), None)
                if owner:
                    if pet_data['species'] == 'Dog':
                        pet = Dog(pet_data['name'], pet_data['age'], owner, "Unknown")
                    elif pet_data['species'] == 'Cat':
                        pet = Cat(pet_data['name'], pet_data['age'], owner, True)
                    else:
                        continue

                    if pet_data['vaccinated']:
                        pet.mark_as_vaccinated()

                    self.add_pet(pet)
        except FileNotFoundError:
            print("No existing data file found. Starting with an empty system.")
        except json.JSONDecodeError:
            print("Error reading the data file. Starting with an empty system.")
