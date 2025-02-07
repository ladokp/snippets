"""
Excuse Generator Module

This module provides a function to generate random funny excuses.
It is intended to bring a bit of humor to everyday situations where an excuse might be needed.
"""

import secrets

EXCUSES = (
    "A squirrel stole my internet cable.",
    "I accidentally formatted my laptop instead of my USB stick.",
    "I discovered a time loop and lost track of time.",
    "I ran out of semicolons.",
    "I thought today was a public holiday.",
    "I was debugging Schrödinger's cat's behavior.",
    "I was stuck in a never-ending Teams meeting.",
    "My ferret ate the code.",
    "My neighbor's parrot kept shouting syntax errors at me.",
    "The coffee machine broke, so I couldn't function."
)

def generate_excuse():
    """
    Function to print a random excuse for today.
    """
    return secrets.choice(EXCUSES)

if __name__ == "__main__":
    print("Excuse for today:", generate_excuse())
