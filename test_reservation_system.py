"""
Pruebas unitarias para el Sistema de Reservaciones de Hotel.
Asegura una cobertura >85% y valida múltiples casos negativos.
"""

import unittest
import os
from reservation_system import Hotel, Customer, Reservation, load_data


class BaseTestCase(unittest.TestCase):
    """Clase base con configuración común para las pruebas."""

    def setUp(self):
        """Configura el entorno de prueba limpiando los archivos de datos."""
        self.clean_up_files()

    def tearDown(self):
        """Limpia los archivos de datos después de cada prueba."""
        self.clean_up_files()

    def clean_up_files(self):
        """Función auxiliar para eliminar archivos JSON
        y asegurar estado limpio."""
        for filename in [
                Hotel.FILE_NAME, Customer.FILE_NAME, Reservation.FILE_NAME]:
            if os.path.exists(filename):
                os.remove(filename)


class TestHotel(BaseTestCase):
    """Casos de prueba para la clase Hotel."""

    def test_create_hotel_success(self):
        """Prueba la creación de un hotel válido."""
        result = Hotel.create_hotel(1, "Hilton", "NY", 100)
        self.assertTrue(result)

    def test_create_hotel_duplicate_negative(self):
        """Prueba Negativa 1: Crea un hotel con un ID ya existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 100)
        result = Hotel.create_hotel(1, "Marriott", "LA", 50)
        self.assertFalse(result)

    def test_delete_hotel_success(self):
        """Prueba la eliminación de un hotel existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 100)
        result = Hotel.delete_hotel(1)
        self.assertTrue(result)

    def test_delete_hotel_not_found_negative(self):
        """Prueba Negativa 2: Eliminar un hotel que no existe."""
        result = Hotel.delete_hotel(99)
        self.assertFalse(result)

    def test_display_hotel_success(self):
        """Prueba mostrar la información de un hotel existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 100)
        result = Hotel.display_hotel(1)
        self.assertEqual(result["name"], "Hilton")

    def test_display_hotel_not_found_negative(self):
        """Prueba Negativa 3: Mostrar un hotel que no existe."""
        result = Hotel.display_hotel(99)
        self.assertIsNone(result)

    def test_modify_hotel_success(self):
        """Prueba modificar los atributos de un hotel existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 100)
        result = Hotel.modify_hotel(1, name="Hilton Updated", rooms=150)
        self.assertTrue(result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["name"], "Hilton Updated")
        self.assertEqual(hotel["rooms"], 150)

    def test_modify_hotel_not_found_negative(self):
        """Prueba Negativa 4: Modificar un hotel que no existe."""
        result = Hotel.modify_hotel(99, name="Ghost")
        self.assertFalse(result)

    def test_hotel_init(self):
        """Prueba la inicialización del objeto Hotel."""
        hotel = Hotel(1, "Hilton", "NY", 100)
        self.assertEqual(hotel.hotel_id, "1")

    def test_cancel_room_invalid_hotel_negative(self):
        """Prueba Negativa 15: Cancelar habitación en hotel
        inexistente directamente."""
        result = Hotel.cancel_room(99)
        self.assertFalse(result)


class TestCustomer(BaseTestCase):
    """Casos de prueba para la clase Customer."""

    def test_create_customer_success(self):
        """Prueba la creación de un cliente válido."""
        result = Customer.create_customer(1, "John Doe", "john@test.com")
        self.assertTrue(result)

    def test_create_customer_duplicate_negative(self):
        """Prueba Negativa 5: Crear un cliente con un ID ya existente."""
        Customer.create_customer(1, "John Doe", "john@test.com")
        result = Customer.create_customer(1, "Jane", "jane@test.com")
        self.assertFalse(result)

    def test_delete_customer_success(self):
        """Prueba la eliminación de un cliente existente."""
        Customer.create_customer(1, "John Doe", "john@test.com")
        result = Customer.delete_customer(1)
        self.assertTrue(result)

    def test_delete_customer_not_found_negative(self):
        """Prueba Negativa 6: Eliminar un cliente que no existe."""
        result = Customer.delete_customer(99)
        self.assertFalse(result)

    def test_display_customer_success(self):
        """Prueba mostrar un cliente existente."""
        Customer.create_customer(1, "John Doe", "john@test.com")
        result = Customer.display_customer(1)
        self.assertEqual(result["name"], "John Doe")

    def test_display_customer_not_found_negative(self):
        """Prueba Negativa 7: Mostrar un cliente que no existe."""
        result = Customer.display_customer(99)
        self.assertIsNone(result)

    def test_modify_customer_success(self):
        """Prueba modificar los atributos de un cliente existente."""
        Customer.create_customer(1, "John", "john@test.com")
        result = Customer.modify_customer(1, name="John D", email="j@test.com")
        self.assertTrue(result)
        customer = Customer.display_customer(1)
        self.assertEqual(customer["name"], "John D")

    def test_modify_customer_not_found_negative(self):
        """Prueba Negativa 8: Modificar un cliente que no existe."""
        result = Customer.modify_customer(99, name="Ghost")
        self.assertFalse(result)


class TestReservation(BaseTestCase):
    """Casos de prueba para la clase Reservation."""

    def test_create_reservation_success(self):
        """Prueba la creación de una reservación válida."""
        Hotel.create_hotel(1, "Hilton", "NY", 10)
        Customer.create_customer(1, "John", "john@test.com")
        result = Reservation.create_reservation(1, 1, 1)
        self.assertTrue(result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["rooms"], 9)

    def test_create_reservation_duplicate_negative(self):
        """Prueba Negativa 9: Crear una reservación con un ID ya existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 10)
        Customer.create_customer(1, "John", "john@test.com")
        Reservation.create_reservation(1, 1, 1)
        result = Reservation.create_reservation(1, 1, 1)
        self.assertFalse(result)

    def test_create_reservation_invalid_customer_negative(self):
        """Prueba Negativa 10: Reservar con un cliente que no existe."""
        Hotel.create_hotel(1, "Hilton", "NY", 10)
        result = Reservation.create_reservation(1, 99, 1)
        self.assertFalse(result)

    def test_create_reservation_invalid_hotel_negative(self):
        """Prueba Negativa 11: Reservar en un hotel que no existe."""
        Customer.create_customer(1, "John", "john@test.com")
        result = Reservation.create_reservation(1, 1, 99)
        self.assertFalse(result)

    def test_create_reservation_no_rooms_negative(self):
        """Prueba Negativa 12: Reservar cuando hay 0
        habitaciones disponibles."""
        Hotel.create_hotel(1, "Hilton", "NY", 0)
        Customer.create_customer(1, "John", "john@test.com")
        result = Reservation.create_reservation(1, 1, 1)
        self.assertFalse(result)

    def test_cancel_reservation_success(self):
        """Prueba la cancelación de una reservación existente."""
        Hotel.create_hotel(1, "Hilton", "NY", 10)
        Customer.create_customer(1, "John", "john@test.com")
        Reservation.create_reservation(1, 1, 1)
        result = Reservation.cancel_reservation(1)
        self.assertTrue(result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["rooms"], 10)

    def test_cancel_reservation_not_found_negative(self):
        """Prueba Negativa 13: Cancelar una reservación que no existe."""
        result = Reservation.cancel_reservation(99)
        self.assertFalse(result)


class TestErrorHandling(BaseTestCase):
    """Casos de prueba para manejo de errores y casos extremos."""

    def setUp(self):
        """Configura el entorno incluyendo archivo corrupto."""
        super().setUp()
        with open("corrupted.json", "w", encoding="utf-8") as file:
            file.write("{invalid_json: data")

    def tearDown(self):
        """Limpia archivos incluyendo el corrupto."""
        super().tearDown()
        if os.path.exists("corrupted.json"):
            os.remove("corrupted.json")

    def test_load_corrupted_json_negative(self):
        """Prueba Negativa 14: Cargar un archivo JSON corrupto."""
        result = load_data("corrupted.json")
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
