import turtle
import math
import time

# Configuración inicial
screen = turtle.Screen()
screen.bgcolor("white")
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.color("red")

# Función para dibujar el corazón en forma circular
def draw_heart_lines():
    pen.penup()
    num_lines = 100
    for i in range(num_lines):
        t = 2 * math.pi * i / num_lines
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        x *= 10
        y *= 10

        pen.goto(0, 0)
        pen.pendown()
        pen.goto(x, y)
        pen.penup()
        time.sleep(0.01)  # Da efecto de animación

# Dibujar el contorno del corazón
def draw_heart_outline():
    pen.pensize(2)
    pen.color("darkred")
    pen.penup()
    t = 0
    x = 16 * math.sin(t) ** 3 * 10
    y = (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 10
    pen.goto(x, y)
    pen.pendown()
    for i in range(101):
        t = 2 * math.pi * i / 100
        x = 16 * math.sin(t) ** 3 * 10
        y = (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 10
        pen.goto(x, y)

# Escribir mensaje
def write_message():
    pen.penup()
    pen.goto(0, -230)
    pen.color("darkmagenta")
    pen.write("TE AMO DANNA", align="center", font=("Arial", 18, "bold"))

# Ejecutar funciones
draw_heart_lines()
draw_heart_outline()
write_message()

# Mantener ventana abierta
screen.mainloop()