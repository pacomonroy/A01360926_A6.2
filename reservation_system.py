"""
Módulo para el Sistema de Reservaciones de Hotel.
Incluye clases para gestionar Hoteles, Clientes (Customers) y Reservaciones
con almacenamiento persistente usando archivos JSON.
"""

import json
import os


def load_data(filename):
    """
    Carga los datos desde un archivo JSON.
    Devuelve un diccionario vacío si el archivo no existe o tiene datos inválidos.
    """
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Datos JSON inválidos en {filename}. Retornando vacío.")
        return {}


def save_data(filename, data):
    """
    Guarda un diccionario en un archivo JSON.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


class Hotel:
    """Clase que representa la entidad Hotel y sus operaciones."""
    FILE_NAME = "hotels.json"

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location
        self.rooms = int(rooms)

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Crea un nuevo hotel y lo guarda en el archivo."""
        data = load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            print(f"Error: El ID del hotel {hotel_id} ya existe.")
            return False
        data[str(hotel_id)] = {
            "name": name,
            "location": location,
            "rooms": rooms
        }
        save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        data = load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            del data[str(hotel_id)]
            save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Hotel con ID {hotel_id} no encontrado.")
        return False

    @classmethod
    def display_hotel(cls, hotel_id):
        """Muestra y devuelve la información del hotel."""
        data = load_data(cls.FILE_NAME)
        hotel = data.get(str(hotel_id))
        if hotel:
            print(f"Hotel {hotel_id}: {hotel}")
            return hotel
        print(f"Error: Hotel con ID {hotel_id} no encontrado.")
        return None

    @classmethod
    def modify_hotel(cls, hotel_id, name=None, location=None, rooms=None):
        """Modifica los atributos de un hotel existente."""
        data = load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            if name is not None:
                data[str(hotel_id)]["name"] = name
            if location is not None:
                data[str(hotel_id)]["location"] = location
            if rooms is not None:
                data[str(hotel_id)]["rooms"] = rooms
            save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Hotel con ID {hotel_id} no encontrado.")
        return False

    @classmethod
    def reserve_room(cls, hotel_id):
        """Disminuye las habitaciones disponibles de un hotel en uno."""
        data = load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            if data[str(hotel_id)]["rooms"] > 0:
                data[str(hotel_id)]["rooms"] -= 1
                save_data(cls.FILE_NAME, data)
                return True
            print(f"Error: No hay habitaciones disponibles en {hotel_id}.")
            return False
        print(f"Error: Hotel con ID {hotel_id} no encontrado.")
        return False

    @classmethod
    def cancel_room(cls, hotel_id):
        """Aumenta las habitaciones disponibles de un hotel en uno."""
        data = load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            data[str(hotel_id)]["rooms"] += 1
            save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Hotel con ID {hotel_id} no encontrado.")
        return False


class Customer:
    """Clase que representa la entidad Customer (Cliente) y sus operaciones."""
    FILE_NAME = "customers.json"

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un nuevo cliente y lo guarda en el archivo."""
        data = load_data(cls.FILE_NAME)
        if str(customer_id) in data:
            print(f"Error: El ID del cliente {customer_id} ya existe.")
            return False
        data[str(customer_id)] = {"name": name, "email": email}
        save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente por su ID."""
        data = load_data(cls.FILE_NAME)
        if str(customer_id) in data:
            del data[str(customer_id)]
            save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Cliente con ID {customer_id} no encontrado.")
        return False

    @classmethod
    def display_customer(cls, customer_id):
        """Muestra y devuelve la información del cliente."""
        data = load_data(cls.FILE_NAME)
        customer = data.get(str(customer_id))
        if customer:
            print(f"Cliente {customer_id}: {customer}")
            return customer
        print(f"Error: Cliente con ID {customer_id} no encontrado.")
        return None

    @classmethod
    def modify_customer(cls, customer_id, name=None, email=None):
        """Modifica los atributos de un cliente existente."""
        data = load_data(cls.FILE_NAME)
        if str(customer_id) in data:
            if name is not None:
                data[str(customer_id)]["name"] = name
            if email is not None:
                data[str(customer_id)]["email"] = email
            save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Cliente con ID {customer_id} no encontrado.")
        return False


class Reservation:
    """Clase que representa la Reservación y sus operaciones."""
    FILE_NAME = "reservations.json"

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Crea una reservación si el cliente existe y hay cuartos libres."""
        customer_data = load_data(Customer.FILE_NAME)
        hotel_data = load_data(Hotel.FILE_NAME)
        res_data = load_data(cls.FILE_NAME)

        if str(reservation_id) in res_data:
            print(f"Error: La reservación {reservation_id} ya existe.")
            return False
        if str(customer_id) not in customer_data:
            print(f"Error: El cliente {customer_id} no existe.")
            return False
        if str(hotel_id) not in hotel_data:
            print(f"Error: El hotel {hotel_id} no existe.")
            return False

        # Intenta reservar la habitación en el hotel
        if Hotel.reserve_room(hotel_id):
            res_data[str(reservation_id)] = {
                "customer_id": str(customer_id),
                "hotel_id": str(hotel_id)
            }
            save_data(cls.FILE_NAME, res_data)
            return True
        return False

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación existente y libera la habitación."""
        res_data = load_data(cls.FILE_NAME)
        if str(reservation_id) in res_data:
            hotel_id = res_data[str(reservation_id)]["hotel_id"]
            Hotel.cancel_room(hotel_id)
            del res_data[str(reservation_id)]
            save_data(cls.FILE_NAME, res_data)
            return True
        print(f"Error: Reservación {reservation_id} no encontrada.")
        return False