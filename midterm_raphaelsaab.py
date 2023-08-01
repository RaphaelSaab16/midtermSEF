import csv
from datetime import datetime, date

class Ticket:
    last_ticket_id = 0


    def __init__(self, ticket_id, event_id, username, date, priority):
        self.ticket_id = ticket_id
        self.event_id = event_id
        self.username = username
        self.date = datetime.strptime(date, '%Y%m%d')
        self.priority = int(priority)

    def get_ticket_id(self):
        return self.ticket_id

    def get_event_id(self):
        return self.event_id

    def get_username(self):
        return self.username

    def get_date(self):
        return self.date

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def __str__(self):
        return f"Ticket ID: {self.ticket_id}, Event ID: {self.event_id}, Username: {self.username}, Date: {self.date.strftime('%Y-%m-%d')}, Priority: {self.priority}"

    def __repr__(self):
        return str(self)


class TicketingSystem:
    def __init__(self):
        self.tickets = []
        self.last_ticket_id = 0  # Initialize last ticket ID
    
    def set_logged_in_user(self, username):
        # Set the username of the logged-in user
        self.logged_in_username = username
    

    def generate_next_ticket_id(self):
            # Generate the next ticket ID by incrementing the last ticket ID by one
        # and checking if it already exists in the list of tickets
        while True:
            self.last_ticket_id += 1
            ticket_id = f"tick{self.last_ticket_id:03d}"
            if not any(ticket.get_ticket_id() == ticket_id for ticket in self.tickets):
                return ticket_id


    def import_tickets(self, file_path):
        """
            Import tickets from a CSV file and add them to the ticketing system.

        Parameters:
            file_path (str): The path to the CSV file containing the tickets data.

        Note:
            The CSV file should be in the format:
            ticket_id, event_id, username, date (YYYYMMDD), priority
        """
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                ticket = Ticket(*row)
                self.tickets.append(ticket)
    
    def is_valid_date(self, date_str):
        """
        Validate if a date string is in the correct format and represents a valid date.

        Parameters:
            date_str (str): The date string to validate in the format 'YYYYMMDD'.

        Returns:
            bool: True if the date string is valid, False otherwise.
        """
        try:
            date = datetime.strptime(date_str, '%Y%m%d')
            year, month, day = date.year, date.month, date.day

            if month < 1 or month > 12:
                return False

            # Check for months with 30 and 31 days
            if month in {1, 3, 5, 7, 8, 10, 12} and (day < 1 or day > 31):
                return False
            elif month in {4, 6, 9, 11} and (day < 1 or day > 30):
                return False
            elif month == 2:
                # Check for leap years and February
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if day < 1 or day > 29:
                        return False
                elif day < 1 or day > 28:
                    return False

            return True
        except ValueError:
            return False

    def get_today_events(self):
        """
        Get the events scheduled for today.

        Returns:
            list: A list of Ticket objects representing today's events.
        """
        # Get the events scheduled for today
        today = date.today()
        today_events = []

        for ticket in self.tickets:
            if ticket.date.date() == today:
                today_events.append(ticket)

        return today_events

    
    def bubble_sort_tickets(self):
        """
        Sort the tickets based on event date and event ID using bubble sort.
        """
        # Bubble sort tickets based on event date and event ID
        n = len(self.tickets)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.compare_tickets(self.tickets[j], self.tickets[j+1]) > 0:
                    # Swap tickets
                    self.tickets[j], self.tickets[j+1] = self.tickets[j+1], self.tickets[j]

    def compare_tickets(self, ticket1, ticket2):
        """
        Compare two tickets based on event date and event ID.

        Parameters:
            ticket1 (Ticket): The first ticket to compare.
            ticket2 (Ticket): The second ticket to compare.

        Returns:
            int: -1 if ticket1 is before ticket2, 1 if ticket1 is after ticket2,
                 and 0 if both tickets have the same date and event ID.
        """
        # Compare tickets based on event date and event ID
        if ticket1.get_date() < ticket2.get_date():
            return -1
        elif ticket1.get_date() > ticket2.get_date():
            return 1
        else:
            if ticket1.get_event_id() < ticket2.get_event_id():
                return -1
            elif ticket1.get_event_id() > ticket2.get_event_id():
                return 1
            else:
                return 0

    def display_statistics(self):
        """
        Display statistics about the tickets, such as the event ID with the highest number of tickets.
        """
        # Get the event ID with the highest number of tickets
        event_id_counts = {}
        for ticket in self.tickets:
            event_id_counts[ticket.get_event_id()] = event_id_counts.get(ticket.get_event_id(), 0) + 1

        if event_id_counts:
            max_event_id = max(event_id_counts, key=event_id_counts.get)
            print(f"The event ID with the highest number of tickets is: {max_event_id}")
        else:
            print("No tickets available.")

  
    def book_ticket(self, event_id, date, priority):
        
        # Book a new ticket for the specified event
        ticket_id = self.generate_next_ticket_id()
        username = self.logged_in_username

        # Create a new Ticket object
        ticket = Ticket(ticket_id, event_id, username, date, priority)

        # Add the new ticket to the list
        self.tickets.append(ticket)
        print("Ticket booked successfully!")


    def display_all_tickets(self):
        # Display all tickets ordered by event's date and event ID using bubble sort
        self.bubble_sort_tickets()

        if self.tickets:
            print("Tickets:")
            for ticket in self.tickets:
                print(ticket)
        else:
            print("No tickets available.")


    def change_ticket_priority(self, ticket_id, new_priority):
        # Change the priority of a ticket by specifying the ticket ID
        found_ticket = None
        for ticket in self.tickets:
            if ticket.get_ticket_id() == ticket_id:
                found_ticket = ticket
                break

        if found_ticket:
            found_ticket.set_priority(new_priority)
            print(f"Priority of Ticket {ticket_id} changed to {new_priority}.")
        else:
            print(f"Ticket {ticket_id} not found.")

    def disable_ticket(self, ticket_id):
        # Remove a ticket from the system
        for ticket in self.tickets:
            if ticket.get_ticket_id() == ticket_id:
                self.tickets.remove(ticket)
                print(f"Ticket {ticket_id} removed successfully.")
                break
        else:
            print(f"Ticket {ticket_id} not found.")

    def run_events(self):
        # Display today's events sorted by priority and remove them from the ticket list
        today_events = self.get_today_events()

        if not today_events:
            print("No events scheduled for today.")
            return
        # Manually sort today's events by priority (higher priority first)
        for i in range(len(today_events)):
            for j in range(0, len(today_events)-i-1):
                if today_events[j].get_priority() < today_events[j+1].get_priority():
                    today_events[j], today_events[j+1] = today_events[j+1], today_events[j]

        print("Today's Events (Sorted by Priority):")
        for ticket in today_events:
            print(f"Event ID: {ticket.get_event_id()}, Priority: {ticket.get_priority()}")
        # Remove today's events from the ticket list
        self.tickets = [ticket for ticket in self.tickets if ticket not in today_events]


    
    
    def user_menu(self):
        # Implement the logic for the normal user menu options
        while True:
            print("\nUser Menu:")
            print("1. Book a Ticket")
            print("2. Exit")

            choice = input("Enter your choice (1-2): ")

            if choice == "1":
                event_id = input("Enter Event ID: ")
                date = input("Enter Date (YYYYMMDD): ")
                priority = 0  # Default priority for normal user
                self.book_ticket(event_id, date, priority)
            elif choice == "2":
                print("Saving tickets and exiting.")
                break
            else:
                print("Invalid choice. Please try again.")
    def admin_menu(self):
        # Implement the logic for the admin menu options
        while True:
            print("\nAdmin Menu:")
            print("1. Display Statistics")
            print("2. Book a Ticket")
            print("3. Display all Tickets")
            print("4. Change Ticket's Priority")
            print("5. Disable Ticket")
            print("6. Run Events")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self.display_statistics()
            elif choice == "2":
                event_id = input("Enter Event ID: ")
                date = input("Enter Date (YYYYMMDD): ")
                priority = int(input("Enter Priority: "))
                self.book_ticket(event_id, date, priority)
            elif choice == "3":
                self.display_all_tickets()
            elif choice == "4":
                ticket_id = input("Enter Ticket ID: ")
                priority = int(input("Enter New Priority: "))
                self.change_ticket_priority(ticket_id, priority)
            elif choice == "5":
                ticket_id = input("Enter Ticket ID: ")
                self.disable_ticket(ticket_id)
            elif choice == "6":
                self.run_events()
            elif choice == "7":
                print("Exiting Admin Menu.")
                break
            else:
                print("Invalid choice. Please try again.")
    def save_tickets(self, file_path):
        # Save the current list of tickets back to a file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for ticket in self.tickets:
                writer.writerow(
                            [ticket.get_ticket_id(), ticket.get_event_id(),ticket.get_username(), ticket.get_date().strftime('%Y%m%d'),ticket.get_priority()]
                    )

def login():
    # Implement the login form and return the user type (admin or normal user)
    max_attempts = 5
    attempts = 0
    admin_username = "admin"
    admin_password = "admin123123"

    while attempts < max_attempts:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username.lower() == admin_username and password == admin_password:
            return "admin"
        elif username and not password:
            return "user"
        else:
            attempts += 1
            print("Incorrect Username and/or Password. Please try again.")

    print("Maximum login attempts exceeded.")
    exit()



def main():
    ticketing_system = TicketingSystem()
    ticketing_system.import_tickets('tickets.txt')
   
    user_type = login()
    if user_type == "admin":
            ticketing_system.set_logged_in_user("admin")
            ticketing_system.admin_menu()
    else:
        # For normal users, set the logged-in username obtained from login form
            ticketing_system.set_logged_in_user("user")
            ticketing_system.user_menu()

    # Save the tickets after the user exits the program (either admin or user)
    ticketing_system.save_tickets('tickets.txt')
if __name__ == "__main__":
    main()