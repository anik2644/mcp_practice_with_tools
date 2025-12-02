from datetime import datetime


# Define the tools (dummy methods)
def get_current_time():
    """Returns the current date and time"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time: {current_time}"

def get_my_address():
    """Returns a dummy address"""
    return "123 Main Street, Suite 456, San Francisco, CA 94105, United States"

def get_my_personal_details():
    """Returns dummy personal details"""
    return {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "occupation": "Software Engineer"
    }

