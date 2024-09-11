import random
import string
import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_insert(self):
        # Generate a random seat
        self.set_seat()

    def set_seat(self):
        random_number = random.randint(1, 99)
        random_letter = random.choice(string.ascii_uppercase[:5])  # A to E
        self.seat = f"{random_number}{random_letter}"

    def validate(self):
        self.calculate_total_amount()
        self.remove_duplicate_add_ons()
        self.check_submission_status()

    def calculate_total_amount(self):
        # Initialize the total amount with the flight price
        total_amount = self.flight_price

        # Sum the amounts from the add-ons
        if self.add_ons:
            for add_on in self.add_ons:
                total_amount += add_on.amount

        # Set the total amount in the document
        self.total_amount = total_amount

    def remove_duplicate_add_ons(self):
        seen_add_ons = set()
        unique_add_ons = []

        for add_on in self.add_ons:
            if add_on.item in seen_add_ons:
                frappe.throw(f"Duplicate Add-On: {add_on.item} cannot be added more than once.")
            seen_add_ons.add(add_on.item)
            unique_add_ons.append(add_on)

        # Replace the add_ons list with the unique add-ons list
        self.add_ons = unique_add_ons

    def check_submission_status(self):
        # Prevent submission if the status is not 'Boarded'
        if self.docstatus == 1 and self.status != "Boarded":
            frappe.throw("The Airplane Ticket cannot be submitted unless the status is 'Boarded'.")
