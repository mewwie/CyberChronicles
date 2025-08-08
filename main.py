from pii_redactor import redact_pii

def main():
    """
    A simple RPG-like text input example.
    """
    print("Welcome to CyberChronicles!")
    print("You are a traveler in a vast digital world.")
    print("What is your story? (Enter your character's backstory)")

    backstory = input("> ")

    redacted_backstory = redact_pii(backstory)

    print("\n--- Your Redacted Backstory ---")
    print(redacted_backstory)
    print("---------------------------------")
    print("\nYour story has been recorded, keeping your personal information safe.")

if __name__ == "__main__":
    main()
