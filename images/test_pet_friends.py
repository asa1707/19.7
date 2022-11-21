import os
from api import PetFriends
from settings import (valid_email, 
                      valid_password, 
                      not_valid_email, 
                      not_valid_password)


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_not_valid_email_and_password(
    email=not_valid_email,
    password=not_valid_password
):

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)


    if not my_pets['pets']:
        pf.add_new_pet(auth_key, "Проглот", "Проглот", "3", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)


    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)


    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)


    assert status == 200
    assert pet_id not in [pet['id'] for pet in my_pets['pets']]


def test_successful_update_self_pet_info(
    name='имя',
    animal_type='животное',
    age=2
):


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, 
                                        pet_id, 
                                        name, 
                                        animal_type, 
                                        age)


    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)


def test_rejection_update_self_pet_info_without_name(
    name='', 
    animal_type='змейка',
    age=2
):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )


    assert status == 200
    assert result['name']


def test_rejection_update_self_pet_info_without_animal_type(
    name='пончик',
    animal_type='', 
    age=1
):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )

    assert status == 200
    assert result['animal_type']


def test_succsessful_update_self_pet_info_with_spase_name(
    name=' ', 
    animal_type='котопес',
    age=1
):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )

    assert status == 200
    assert result['name'] == ' '


def test_add_new_pet_with_valid_data_without_foto(
    name='водород',
    animal_type='дым',
    age='4'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, 
        name, 
        animal_type, 
        age)


    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_incorrect_data_without_foto(
    name='_+-$%^&!*',
    animal_type='', 
    age=''
):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, 
        name, 
        animal_type, 
        age
    )

    assert status == 200
    assert result['name'] == name


def test_successful_add_foto_of_pet(
    pet_id='', 
    pet_photo ='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo']