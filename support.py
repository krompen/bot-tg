import telebot

class SupportTicketSystem:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.tickets = {}

    def start_support(self, message):
        self.bot.reply_to(message, "Welcome to the support ticket system! Please describe your issue.")

    def create_ticket(self, user_id, issue):
        ticket_id = len(self.tickets) + 1
        self.tickets[ticket_id] = {'user_id': user_id, 'issue': issue, 'status': 'open'}
        return ticket_id

    @self.bot.message_handler(commands=['start'])
    def handle_start(message):
        self.start_support(message)

    @self.bot.message_handler(func=lambda message: True)
    def handle_message(message):
        ticket_id = self.create_ticket(message.from_user.id, message.text)
        self.bot.reply_to(message, f"Your ticket has been created! Ticket ID: {ticket_id}")

    def run(self):
        self.bot.polling()  

# Example usage
# token = 'YOUR_TELEGRAM_BOT_TOKEN'
# support_system = SupportTicketSystem(token)
# support_system.run()