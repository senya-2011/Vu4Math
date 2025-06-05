from flask import Flask, render_template, request, send_file, redirect
import math
import io, base64

from logic.euler import solve_euler, runge_error as runge_error_euler
from logic.runge_kutta import solve_rk4, runge_error as runge_error_rk4
from logic.adams import solve_adams4, max_error_adams

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# --- ОДУ с точными решениями ---
def ode1():
    def f(x, y):
        return y
    def exact(x, x0, y0):
        return y0 * math.exp(x - x0)
    desc = "y' = y"
    return f, exact, desc

def ode2():
    def f(x, y):
        return x - 2*y
    def exact(x, x0, y0):
        C = y0 - (x0/2 - 0.25)
        return x/2 - 0.25 + C * math.exp(-2*(x - x0))
    desc = "y' = x - 2y"
    return f, exact, desc

def ode3():
    def f(x, y):
        return x * (1 - x)
    def exact(x, x0, y0):
        return y0 + (x**2/2 - x**3/3) - (x0**2/2 - x0**3/3)
    desc = "y' = x*(1 - x)"
    return f, exact, desc

def choose_ode(ode_choice):
    if ode_choice == '1':
        return ode1()
    elif ode_choice == '2':
        return ode2()
    elif ode_choice == '3':
        return ode3()
    else:
        return ode1()

def convert_to_float(val_str, default=0.0):
    if not val_str:
        return default
    val_str = val_str.replace(',', '.')
    try:
        return float(val_str)
    except ValueError:
        return default

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    ode_choice = request.form.get('ode')
    x0 = convert_to_float(request.form.get('x0', '0.0'))
    y0 = convert_to_float(request.form.get('y0', '1.0'))
    xn = convert_to_float(request.form.get('xn', '1.0'))
    h  = convert_to_float(request.form.get('h', '0.1'))
    eps = convert_to_float(request.form.get('eps', '0.01'))
    methods = request.form.getlist('methods')

    # Валидация входных данных
    if h <= 0:
        return render_template('error.html', message="Шаг h должен быть положительным и отличным от нуля.")
    if x0 > xn:
        return render_template('error.html', message="Начальная точка x₀ не должна быть больше конечной xn.")

    f, exact_func, ode_desc = choose_ode(ode_choice)

    xs = None
    solutions = []
    ys_exact = None

    report_lines = []
    report_lines.append(f"Задача: {ode_desc}")
    report_lines.append(f"x0 = {x0}, y0 = {y0}, xn = {xn}, h = {h}, eps = {eps}")
    report_lines.append("Методы и оценки погрешностей:")

    for m in methods:
        if m == '1':
            xs_e, ys_e = solve_euler(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_e
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            err_est = runge_error_euler(f, x0, y0, xn, h, solve_euler, p=1)
            status = 'success' if err_est <= eps else 'danger'
            solutions.append((ys_e, "Эйлер", err_est, status))
        elif m == '2':
            xs_rk, ys_rk = solve_rk4(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_rk
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            err_est = runge_error_rk4(f, x0, y0, xn, h, solve_rk4, p=4)
            status = 'success' if err_est <= eps else 'danger'
            solutions.append((ys_rk, "РК4", err_est, status))
        elif m == '3':
            xs_ad, ys_ad = solve_adams4(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_ad
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            max_err = max_error_adams(lambda x: exact_func(x, x0, y0), xs_ad, ys_ad)
            status = 'success' if max_err <= eps else 'danger'
            solutions.append((ys_ad, "Адамс", max_err, status))

    # Общий график
    fig = plt.figure()
    plt.plot(xs, ys_exact, linestyle='-', color='black', label='Точное')
    markers = ['o', 's', '^']
    linestyles = ['--', '-.', ':']
    for idx, (ys_num, label, err_val, status) in enumerate(solutions):
        plt.plot(xs, ys_num,
                 linestyle=linestyles[idx % len(linestyles)],
                 marker=markers[idx % len(markers)],
                 label=label)
    plt.title(f"{ode_desc}, h={h}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    combined_graph = base64.b64encode(buf.getvalue()).decode('utf8')

    report_lines.append("")
    header = ["x".ljust(8)]
    for _, label, _, _ in solutions:
        header.append(label.ljust(12))
    header.append("exact".ljust(12))
    report_lines.append(" | ".join(header))
    report_lines.append("-" * (len(report_lines[-1]) + 3))

    combined_rows = []
    for i, xi in enumerate(xs):
        row = {'x': f"{xi:.3f}"}
        row_list = [f"{xi:<8.3f}"]
        for ys_num, label, _, _ in solutions:
            val = f"{ys_num[i]:<12.3f}"
            row_list.append(val)
            row[label] = f"{ys_num[i]:.3f}"
        exact_val_formatted = f"{ys_exact[i]:<12.3f}"
        row_list.append(exact_val_formatted)
        row['exact'] = f"{ys_exact[i]:.3f}"
        combined_rows.append(row)
        report_lines.append(" | ".join(row_list))

    report_text = "\n".join(report_lines)

    per_method = []
    for idx, (ys_num, label, err_val, status) in enumerate(solutions):
        figm = plt.figure()
        plt.plot(xs, ys_exact, linestyle='-', color='black', label='Точное')
        plt.plot(xs, ys_num,
                 linestyle=linestyles[idx % len(linestyles)],
                 marker=markers[idx % len(markers)],
                 label=label)
        plt.title(f"{label}, {ode_desc}, h={h}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        bufm = io.BytesIO()
        plt.savefig(bufm, format='png')
        bufm.seek(0)
        plt.close(figm)
        graph_m = base64.b64encode(bufm.getvalue()).decode('utf8')

        rows = []
        for i, xi in enumerate(xs):
            rows.append((f"{xi:.3f}", f"{ys_num[i]:.3f}", f"{ys_exact[i]:.3f}"))

        per_method.append({
            'label': label,
            'error_value': err_val,
            'error_status': status,
            'graph': graph_m,
            'rows': rows
        })

    return render_template(
        'results.html',
        ode_desc=ode_desc,
        x0=f"{x0:.3f}", y0=f"{y0:.3f}",
        xn=f"{xn:.3f}", h=f"{h:.3f}", eps=f"{eps}",
        combined_graph=combined_graph,
        combined_rows=combined_rows,
        solutions=solutions,
        per_method=per_method,
        report_text=report_text
    )

@app.route('/download_report', methods=['POST'])
def download_report():
    report_text = request.form.get('report_content', '')
    buf = io.BytesIO()
    buf.write(report_text.encode('utf-8'))
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name='report.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)