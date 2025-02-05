import random

def generate_excuse():
    excuses = (
        "My ferret ate the code.",
        "I was stuck in a never-ending Zoom meeting.",
        "I thought today was a public holiday.",
        "I accidentally formatted my laptop instead of my USB stick.",
        "The coffee machine broke, so I couldn't function.",
        "A squirrel stole my internet cable.",
        "I ran out of semicolons.",
        "I discovered a time loop and lost track of time.",
        "I was debugging Schrödinger's cat's behavior.",
        "My neighbor's parrot kept shouting syntax errors at me."
    )
    return random.choice(excuses)

if __name__ == "__main__":
    print("Excuse for today:", generate_excuse())
