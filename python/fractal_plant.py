import turtle

def l_system(axiom, rules, iterations):
    """Generiert ein L-System basierend auf Regeln und Iterationen."""
    for _ in range(iterations):
        axiom = ''.join(rules.get(ch, ch) for ch in axiom)
    return axiom

def draw_l_system(axiom, angle, length):
    """Zeichnet das L-System mit Turtle Graphics."""
    stack = []
    for command in axiom:
        if command == 'F':
            turtle.forward(length)
        elif command == '+':
            turtle.right(angle)
        elif command == '-':
            turtle.left(angle)
        elif command == '[':
            stack.append((turtle.pos(), turtle.heading()))
        elif command == ']':
            pos, heading = stack.pop()
            turtle.penup()
            turtle.setpos(pos)
            turtle.setheading(heading)
            turtle.pendown()

# Regeln für eine einfache Fraktalpflanze
rules = {
    'F': 'FF+[+F-F-F]-[-F+F+F]'
}
axiom = "F"
iterations = 3
angle = 30
length = 11

# L-System generieren und zeichnen
turtle.speed(0)
turtle.left(90)  # Startwinkel nach oben
commands = l_system(axiom, rules, iterations)
draw_l_system(commands, angle, length)
turtle.done()
