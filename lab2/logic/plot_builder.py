import matplotlib
import logic.properties as properties

matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt


def makeplot(f, a, b):
    x_values = np.linspace(a, b, 400)
    y_values = f(x_values)
    plt.plot(x_values, y_values, label=f"f(x)")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'График функции f(x) на отрезке [{a}, {b}]')
    plt.legend()
    save_path = f'C:/rubbish/calcmath/lab2/graph{properties.img_i}.png'
    plt.savefig(save_path)
    plt.close()

def makeplot_system(f1, f2, a, b):
    x = np.linspace(a, b, 400)
    y = np.linspace(a, b, 400)
    X, Y = np.meshgrid(x, y)

    Z1 = f1(X, Y)
    Z2 = f2(X, Y)

    plt.figure(figsize=(6, 6))
    plt.contour(X, Y, Z1, levels=[0], colors='r', label="f1(x, y) = 0")
    plt.contour(X, Y, Z2, levels=[0], colors='b', label="f2(x, y) = 0")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("График системы уравнений")
    plt.grid(True)

    save_path = f'C:/rubbish/calcmath/lab2/graph{properties.img_i}.png'
    plt.savefig(save_path)
    plt.close()
