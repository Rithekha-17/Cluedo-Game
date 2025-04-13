# Clue Game: AI vs Human

Welcome to **Clue Game**, a Python-based strategic deduction game inspired by the classic board game *Clue (Cluedo)*. Compete against a logic-driven AI to deduce the **murderer**, **weapon**, and **location** involved in a fictional crime using reasoning, elimination, and smart questioning.

## Game Objective

Be the first to correctly deduce the hidden solution—one suspect, one weapon, and one location—before the AI does.

---

## Features

- Turn-based gameplay between a human and an AI opponent.
- AI uses Forward Chaining and Knowledge-Based Deduction to eliminate possibilities.
- Interactive GUI built with Tkinter featuring dropdown selections and buttons.
- Randomized solution and card distribution on every game start.
- Win by guessing the correct combination before the AI.

---

## Game Setup

### Categories
- Suspects: Miss Scarlet, Colonel Mustard, Mrs. White, Mr. Green, Mrs. Peacock, Professor Plum  
- Weapons: Knife, Candlestick, Revolver, Rope, Lead Pipe  
- Locations: Hall, Lounge, Kitchen, Ballroom, Conservatory, Attic

### Cards
- One card from each category is randomly selected as the hidden solution.
- The remaining cards are shuffled and distributed equally between the player and the AI.

---

## Installation & Setup

### Requirements

- Python 3.7 or higher (recommended: Python 3.8 or 3.9)
- Libraries:
  - `tkinter` (GUI)
  - `random` (standard)
  - `tkinter.messagebox` (for prompts)

### Installation (if needed)
```bash
# Linux
sudo apt-get install python3-tk

# Windows/macOS
# Tkinter is usually bundled with Python. If not, re-install Python and ensure "tcl/tk" is included.
