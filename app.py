from flask import Flask, render_template, request, redirect, url_for
from pet_management import PetManagementSystem, Owner, Dog, Cat

app = Flask(__name__)
pet_system = PetManagementSystem()


# Put all the Flask route definitions here
# This includes all the code from the second code block in my previous response
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/owners')
def list_owners():
    owners = pet_system.get_all_owners()
    return render_template('owners.html', owners=owners)


@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        owner = Owner(name, phone)
        pet_system.add_owner(owner)
        return redirect(url_for('list_owners'))
    return render_template('add_owner.html')


@app.route('/pets')
def list_pets():
    pets = pet_system.get_all_pets()
    return render_template('pets.html', pets=pets)


@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        age = int(request.form['age'])
        owner_name = request.form['owner']
        vaccinated = 'vaccinated' in request.form

        owner = next((o for o in pet_system.get_all_owners() if o.name == owner_name), None)

        if owner:
            if species == 'Dog':
                breed = request.form['breed']
                pet = Dog(name, age, owner, breed, vaccinated)
            elif species == 'Cat':
                indoor = 'indoor' in request.form
                pet = Cat(name, age, owner, indoor, vaccinated)

            try:
                pet_system.add_pet(pet)
                return redirect(url_for('list_pets'))
            except ValueError as e:
                return render_template('add_pet.html', error=str(e), owners=pet_system.get_all_owners())
        else:
            return render_template('add_pet.html', error="Owner not found", owners=pet_system.get_all_owners())

    return render_template('add_pet.html', owners=pet_system.get_all_owners())


@app.route('/services')
def services():
    return render_template('services.html', pets=pet_system.get_all_pets())


if __name__ == '__main__':
    pet_system.load_from_file()
    app.run(debug=True)
    pet_system.save_to_file()
