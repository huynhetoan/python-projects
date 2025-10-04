import turtle

def draw_triangle(points, color, t):
    t.fillcolor(color)
    t.up()
    t.goto(points[0][0], points[0][1])
    t.down()
    t.begin_fill()
    t.goto(points[1][0], points[1][1])
    t.goto(points[2][0], points[2][1])
    t.goto(points[0][0], points[0][1])
    t.end_fill()

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def sierpinski(points, depth, t):
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    draw_triangle(points, palette[depth % len(palette)], t)
    if depth > 0:
        p0, p1, p2 = points
        sierpinski([p0, midpoint(p0, p1), midpoint(p0, p2)], depth - 1, t)
        sierpinski([p1, midpoint(p1, p0), midpoint(p1, p2)], depth - 1, t)
        sierpinski([p2, midpoint(p2, p0), midpoint(p2, p1)], depth - 1, t)

def main():
    DEPTH = 6  # Increase/decrease for more/less detail
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    screen = turtle.Screen()
    screen.bgcolor("white")

    # Equilateral triangle coordinates
    size = 380
    points = [(-size, -220), (0, -220 + size * 1.732/2), (size, -220)]

    sierpinski(points, DEPTH, t)
    screen.mainloop()

if __name__ == "__main__":
    main()