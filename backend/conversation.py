import re
from storage import get_user, save_user, save_lead

def is_valid_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return 10 <= len(digits) <= 15


def handle_message(user_id: str, text: str):
    user = get_user(user_id)
    msg = text.lower()

    # GREETING
    if msg in ["hi", "hello", "hey", "hi there"]:
        user["step"] = "SERVICE"
        save_user(user)
        return (
            "Hello 👋 Welcome to Sunrise Clinic.\n"
            "How can I help you today?\n"
            "1. Book Appointment\n"
            "2. Clinic Timings"
        )

    if user["step"] == "WELCOME":
        user["step"] = "SERVICE"
        save_user(user)
        return (
            "Hello 👋 Welcome to Sunrise Clinic.\n"
            "How can I help you today?\n"
            "1. Book Appointment\n"
            "2. Clinic Timings"
        )

    if user["step"] == "SERVICE":
        if "1" in msg or "book" in msg or "appointment" in msg:
            user["step"] = "CHOOSE_SERVICE"
            save_user(user)
            return "Which service do you need?\n1. General\n2. Dental\n3. Skin"

        if "2" in msg or "time" in msg:
            return "Clinic timings: Mon–Sat, 9am–6pm"

        return "Please choose:\n1. Book Appointment\n2. Clinic Timings"

    if user["step"] == "CHOOSE_SERVICE":
        user["service"] = text
        user["step"] = "DATE"
        save_user(user)
        return "Please share your preferred date."

    if user["step"] == "DATE":
        user["date"] = text
        user["step"] = "PHONE"
        save_user(user)
        return "Please share your phone number (with country code if possible)."

    if user["step"] == "PHONE":
        if not is_valid_phone(text):
            return "❌ Please enter a valid phone number (10–15 digits)."

        user["phone"] = text
        save_lead(user) 
        user["step"] = "DONE"
        save_user(user)

        return (
            "✅ Thank you!\n"
            "Your appointment request has been received.\n"
            "Our team will contact you shortly."
        )

    return "Thanks for contacting Sunrise Clinic."
