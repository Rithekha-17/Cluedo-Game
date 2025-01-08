import tkinter as tk
from tkinter import messagebox
import random 

# Define the possible cards
suspects = ["Miss Scarlet", "Colonel Mustard", "Dr. Orchid", "Mr. Green", "Mrs. Peacock", "Professor Plum"] 
weapons = ["Knife", "Candlestick", "Revolver", "Rope", "Lead Pipe"] 
locations = ["Hall", "Lounge", "Kitchen", "Ballroom", "Conservatory", "Attic"] 

# Randomly choose the solution cards
solution = {
    "murderer": random.choice(suspects),
    "weapon": random.choice(weapons),
    "location": random.choice(locations)
}
print("For Reference: ")
print("Solution is: ", solution)

# Remove solution cards from the deck
remaining_suspects = [s for s in suspects if s != solution["murderer"]]
remaining_weapons = [w for w in weapons if w != solution["weapon"]]
remaining_locations = [l for l in locations if l != solution["location"]]

# Create a deck with remaining cards
deck = remaining_suspects + remaining_weapons + remaining_locations
random.shuffle(deck)

# Distribute cards to AI and player
ai_cards = deck[:len(deck) // 2]
player_cards = deck[len(deck) // 2:]

# AI knowledge base
ai_knowledge = {
    "suspects": [s for s in suspects if s not in ai_cards],
    "weapons": [w for w in weapons if w not in ai_cards],
    "locations": [l for l in locations if l not in ai_cards],
    "known_murderer": None,
    "known_weapon": None,
    "known_location": None
}

# Initialize tkinter root window
root = tk.Tk()
root.title("Cluedo Deduction Game")
root.geometry("1000x880")
root.configure(bg="lightblue")

# Display text area for game output
display_text = tk.Text(root, height=18, width=70, bg="lightyellow", wrap=tk.WORD, font=("Helvetica", 14))
display_text.pack(pady=10)

# Insert welcome message and instructions
welcome_message = """
Welcome to Cluedo!

Instructions:
1. Try to deduce the correct combination of murderer, weapon, and location.
2. Each turn, ask the AI about specific suspects, weapons, or locations.
3. The AI will reveal a card if it has one, or respond with "No."
4. Use responses to narrow down the possibilities and make an informed guess.

Good luck!
Select Your Cards: 
"""

# Display the message in the text area
display_text.insert(tk.END, welcome_message)

# Show all available cards
all_cards_label = tk.Label(root, text="All Available Cards:", bg="lightblue", font=("Helvetica", 16, "bold"))
all_cards_label.pack()

# Display the suspects, weapons, and locations
suspects_label = tk.Label(root, text=f"Suspects: {', '.join(suspects)}", bg="lightblue", font=("Helvetica", 14))
suspects_label.pack()
weapons_label = tk.Label(root, text=f"Weapons: {', '.join(weapons)}", bg="lightblue", font=("Helvetica", 14))
weapons_label.pack()
locations_label = tk.Label(root, text=f"Locations: {', '.join(locations)}", bg="lightblue", font=("Helvetica", 14))
locations_label.pack()

# Player's cards display label
player_cards_label = tk.Label(root, text=f"Your Cards: {', '.join(player_cards)}", bg="lightblue", font=("Helvetica", 14, "bold"))
player_cards_label.pack(pady=10)

# Insert and auto-scroll the display text
def update_display_text(message):
    display_text.insert(tk.END, message)
    display_text.see(tk.END)  # Auto-scroll to the end

# Display the knowledge base for AI
def print_knowledge_base():
    print("AI Knowledge Base:")
    print(f"Known Murderer: {ai_knowledge['known_murderer']}")
    print(f"Known Weapon: {ai_knowledge['known_weapon']}")
    print(f"Known Location: {ai_knowledge['known_location']}")
    print(f"Remaining Suspects: {ai_knowledge['suspects']}")
    print(f"Remaining Weapons: {ai_knowledge['weapons']}")
    print(f"Remaining Locations: {ai_knowledge['locations']}")
    print("\n")

# Update AI's knowledge base when a card is revealed
def ai_update_knowledge(revealed_card):
    if revealed_card in ai_knowledge["suspects"]:
        ai_knowledge["suspects"].remove(revealed_card)
    if revealed_card in ai_knowledge["weapons"]:
        ai_knowledge["weapons"].remove(revealed_card)
    if revealed_card in ai_knowledge["locations"]:
        ai_knowledge["locations"].remove(revealed_card)
    print_knowledge_base()

# AI deduces based on a "No" response from the player
def ai_deduce(question):
    for card in question:
        if card not in ai_cards:
            if card in suspects:
                ai_knowledge["known_murderer"] = card
            elif card in weapons:
                ai_knowledge["known_weapon"] = card
            elif card in locations:
                ai_knowledge["known_location"] = card
    print_knowledge_base()

# AI's turn using forward chaining (to ask the best cards to the player)
def ai_turn():
    cards_to_ask = []
    if not ai_knowledge["known_murderer"]:
        remaining_suspects = [s for s in ai_knowledge["suspects"] if s not in ai_cards]
        if remaining_suspects:
            cards_to_ask.append(remaining_suspects[0])
    if not ai_knowledge["known_weapon"]:
        remaining_weapons = [w for w in ai_knowledge["weapons"] if w not in ai_cards]
        if remaining_weapons:
            cards_to_ask.append(remaining_weapons[0])
    if not ai_knowledge["known_location"]:
        remaining_locations = [l for l in ai_knowledge["locations"] if l not in ai_cards]
        if remaining_locations:
            cards_to_ask.append(remaining_locations[0])
    return cards_to_ask[:2]

# Check if AI can guess the solution
def ai_check_solution():
    return all([
        ai_knowledge["known_murderer"],
        ai_knowledge["known_weapon"],
        ai_knowledge["known_location"]
    ])

# AI makes a final guess
def ai_make_guess():
    return {
        "murderer": ai_knowledge["known_murderer"],
        "weapon": ai_knowledge["known_weapon"],
        "location": ai_knowledge["known_location"]
    }

# Handle a player's turn
def player_turn():
    question = [player_card1.get(), player_card2.get()]
    response = handle_response(question, ai_cards)
    update_display_text(f"Player asked about: {question}\n")
    if response != "No":
        update_display_text(f"AI reveals: {response}")
    else:
        update_display_text("AI responds: No")
    update_display_text("\n")
    
    # Enable the guess button after the player's turn
    guess_button.config(state=tk.NORMAL)

    # Automatically proceed to AI's turn
    ai_turn_main()

# Handle response for AI and player
def handle_response(question, opponent_cards):
    for card in question:
        if card in opponent_cards:
            return card
    return "No"

# Main game loop for the AI turn
def ai_turn_main():
    question = ai_turn()
    response = handle_response(question, player_cards)
    update_display_text(f"\nAI asks about: {question}\n")
    if response != "No":
        update_display_text(f"Player reveals: {response}\n")
        update_display_text("\nSelect Your Cards:")
        ai_update_knowledge(response)
    else:
        update_display_text("Player responds: No\n")
        update_display_text("\nSelect Your Cards:")
        ai_deduce(question)
    if ai_check_solution():
        ai_guess = ai_make_guess()
        update_display_text(f"AI has deduced the solution!\nThe solution is {ai_guess}\n")
        announce_winner("AI")
    update_display_text("\n")
   
# Function to announce the winner
def announce_winner(winner):
    if winner == "Player":
        messagebox.showinfo("Game Over", "\nCongratulations! You have deduced the correct solution and won the game!")
    else:
        messagebox.showinfo("Game Over\n", f"The AI has won! The correct solution was: {solution}")

# Create dropdown for player card selection
player_card1 = tk.StringVar()
player_card2 = tk.StringVar()

# Dropdown menus for player turn
def create_player_dropdowns():
    tk.Label(root, text="Select your cards:", bg="lightblue").pack(pady=5)
    tk.OptionMenu(root, player_card1, *suspects + weapons + locations).pack()
    tk.OptionMenu(root, player_card2, *suspects + weapons + locations).pack()

def submit_player_turn():
    player_turn()

def guess_solution():
    guess_window = tk.Toplevel(root)
    guess_window.title("Make Your Guess")
    
    tk.Label(guess_window, text="Guess the Murderer:").pack()
    murderer_guess = tk.StringVar()
    tk.OptionMenu(guess_window, murderer_guess, *suspects).pack()

    tk.Label(guess_window, text="Guess the Weapon:").pack()
    weapon_guess = tk.StringVar()
    tk.OptionMenu(guess_window, weapon_guess, *weapons).pack()

    tk.Label(guess_window, text="Guess the Location:").pack()
    location_guess = tk.StringVar()
    tk.OptionMenu(guess_window, location_guess, *locations).pack()

    def submit_guess():
        guess = {
            "murderer": murderer_guess.get(),
            "weapon": weapon_guess.get(),
            "location": location_guess.get()
        }
        if guess == solution:
            announce_winner("Player")
        else:
            announce_winner("AI")
        guess_window.destroy()

    tk.Button(guess_window, text="Submit Guess", command=submit_guess).pack()

# Buttons for submitting player turn and guess
submit_button = tk.Button(root, text="Submit Your Turn", command=submit_player_turn, bg="lightgreen")
submit_button.pack(pady=10)

guess_button = tk.Button(root, text="Make a Guess", command=guess_solution, state=tk.DISABLED)
guess_button.pack()

# Start the game and initialize player dropdowns
create_player_dropdowns()

# Run the tkinter main loop
root.mainloop()