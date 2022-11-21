import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_code_json_or_text(response):
    result = ""
    try:
        result = response.json()
    except json.decoder.JSONDecodeError:
        result = response.text
    return response.status_code, result


class PetFriends:

    BASE_URL = "https://petfriends.skillfactory.ru/"
    ALL_PETS = ""
    MY_PETS = "my_pets"

    def get_api_key(self, email: str, passwd: str) -> json:

        headers = {
            'email': email,
            'password': passwd,
        }
        return get_code_json_or_text(requests.get(
            self.BASE_URL + 'api/key',
            headers=headers))

    def get_list_of_pets(self, auth_key: json,
                         all_or_my_pets: str = "") -> json:

        headers = {'auth_key': auth_key['key']}
        all_or_my_pets = {'filter': all_or_my_pets}

        return get_code_json_or_text(requests.get(
            self.BASE_URL + 'api/pets',
            headers=headers,
            params=all_or_my_pets))

    def add_new_pet(self, auth_key: json,
                    name: str,
                    animal_type: str,
                    age: str,
                    pet_photo: str) -> json:

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (
                    pet_photo,
                    open(pet_photo, 'rb'), 'image/jpeg'
                )
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/pets',
            headers=headers,
            data=data))

    def delete_pet(self, auth_key: json,
                   pet_id: str) -> json:

        headers = {'auth_key': auth_key['key']}

        return get_code_json_or_text(requests.delete(
            self.BASE_URL + 'api/pets/' + pet_id,
            headers=headers))

    def update_pet_info(self,
                        auth_key: json,
                        pet_id: str,
                        name: str,
                        animal_type: str,
                        age: int) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        return get_code_json_or_text(requests.put(
            self.BASE_URL + 'api/pets/' + pet_id,
            headers=headers,
            data=data))

    def add_new_pet_without_photo(self,
                                  auth_key: json,
                                  name: str,
                                  animal_type: str,
                                  age: str) -> json:

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/create_pet_simple',
            headers=headers,
            data=data))

    def add_foto_of_pet(self,
                        auth_key: json,
                        pet_id: str,
                        pet_photo: str) -> json:

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo,
                                  open(pet_photo, 'rb'),
                                  'image/jpeg')})
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/pets/set_photo/' + pet_id,
            headers=headers,
            data=data))