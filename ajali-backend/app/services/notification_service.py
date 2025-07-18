# /app/services/notification_service.py

def send_status_update_notification(incident):
    """
    Placeholder for sending notifications.
    In a real-world app, this would use a service like SendGrid, Twilio, or Firebase Cloud Messaging.
    """
    print(f"--- NOTIFICATION ---")
    print(f"To: User {incident.author.username} ({incident.author.email})")
    print(f"Subject: Status of your report '{incident.title}' has been updated.")
    print(f"The new status is: {incident.status.upper()}")
    print(f"--------------------")
    # This is just a simulation. No actual email is sent.