from flask import Flask, render_template, request, flash, redirect, session, url_for, send_file, abort
from werkzeug.utils import secure_filename
from solution import (
    lagrange, newton_divided, newton_forward, newton_backward,
    gauss_forward, gauss_backward, stirling, bessel, make_plot, GENERATORS
)
from tools.file_reader import read_xy_from_txt_filepath
from tools.math_tools import finite_diff_table
import tools.plot_tool as plot_utils
import os
import io
import base64
import uuid
import atexit
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_SESSION_SIZE'] = 4093  # Максимальный размер сессии
ALLOWED_EXT = {'txt'}

METHODS = {
    'Лагранж': lagrange,
    'Ньютона (разд. разн.)': newton_divided,
    'Ньютона (прям. кон. разн.)': newton_forward,
    'Ньютона (обр. кон. разн.)': newton_backward,
    'Гаусса (вперёд)': gauss_forward,
    'Гаусса (назад)': gauss_backward,
    'Стирлинга': stirling,
    'Бесселя': bessel
}


def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def cleanup_temp():
    temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


atexit.register(cleanup_temp)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mode = request.form.get('input_mode', 'manual')
        x_vals = y_vals = []
        session.pop('generator', None)
        data_id = str(uuid.uuid4())
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        try:
            if mode == 'file':
                f = request.files.get('data_file')
                if not f or not allowed_file(f.filename):
                    flash('Нужен .txt файл', 'danger')
                    return redirect(url_for('index'))

                path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
                f.save(path)
                try:
                    x_vals, y_vals = read_xy_from_txt_filepath(path)
                finally:
                    os.remove(path)

            elif mode == 'manual':
                xs = request.form.get('x_values', '').replace(',', '.').split()
                ys = request.form.get('y_values', '').replace(',', '.').split()

                if not xs or not ys:
                    flash('Введите X и Y', 'warning')
                    return redirect(url_for('index'))

                x_vals = list(map(float, xs))
                y_vals = list(map(float, ys))

            else:
                gen = request.form.get('generator')
                a = request.form.get('interval_start', '').replace(',', '.')
                b = request.form.get('interval_end', '').replace(',', '.')
                n = request.form.get('n_points', '')

                a, b = float(a), float(b)
                n = int(n)
                if n < 2:
                    raise ValueError

                func = GENERATORS.get(gen)
                if not func:
                    flash('Выберите функцию', 'warning')
                    return redirect(url_for('index'))

                session['generator'] = gen
                import numpy as np
                x_vals = list(np.linspace(a, b, n))
                y_vals = [func(x) for x in x_vals]

            # Общие проверки
            if len(x_vals) != len(y_vals) or len(x_vals) < 2:
                flash('Нужно минимум 2 точки', 'danger')
                return redirect(url_for('index'))

            try:
                x0 = float(request.form.get('x_val', '').replace(',', '.'))
            except:
                flash('Неверная точка оценки', 'danger')
                return redirect(url_for('index'))

            sel = request.form.getlist('methods')
            if not sel:
                flash('Выберите методы', 'warning')
                return redirect(url_for('index'))

            # Обработка данных
            diff_table = finite_diff_table(y_vals)
            results = []
            methods_used = {}

            for name in sel:
                func = METHODS[name]
                poly, t = func(x_vals, y_vals, x0)
                p = poly(x0) if poly else None
                results.append({'name': name, 't': t, 'p': p})
                methods_used[name] = func

            # Генерация и сохранение графиков
            fig = make_plot(x_vals, y_vals, x0, methods_used)
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            with open(os.path.join(temp_dir, f'{data_id}_combined.png'), 'wb') as f:
                f.write(buf.getvalue())

            method_files = {}
            for name, func in methods_used.items():
                fig = plot_utils.plot_interpolation(
                    x_vals, y_vals, x0,
                    {name: func}
                )
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                filename = f'{data_id}_{name}.png'
                with open(os.path.join(temp_dir, filename), 'wb') as f:
                    f.write(buf.getvalue())
                method_files[name] = filename

            # Сохраняем только необходимые данные в сессию
            session['results'] = results
            session['diff_table'] = diff_table
            session['x0'] = x0
            session['data_id'] = data_id
            session['method_files'] = method_files

            return redirect(url_for('results'))

        except Exception as e:
            flash(f'Ошибка обработки данных: {str(e)}', 'danger')
            return redirect(url_for('index'))

    return render_template('index.html',
                           methods=list(METHODS.keys()),
                           generators=list(GENERATORS.keys()))


@app.route('/results')
def results():
    return render_template('results.html',
                           results=session.get('results', []),
                           diff_table=session.get('diff_table', []),
                           x0=session.get('x0'),
                           data_id=session.get('data_id'),
                           method_files=session.get('method_files', {})
                           )


@app.route('/temp/<data_id>/<filename>')
def get_temp_image(data_id, filename):
    temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
    path = os.path.join(temp_dir, f'{data_id}_{filename}')
    if os.path.exists(path):
        return send_file(path, mimetype='image/png')



@app.route('/download-report')
def download_report():
    results = session.get('results', [])
    diff = session.get('diff_table', [])
    x0 = session.get('x0', '')

    buf = io.StringIO()
    buf.write("\nDiffs:\n")
    for row in diff:
        buf.write('\t'.join(map(str, row)) + '\n')  # важно: без вложенности

    buf.write(f"\nResults at x={x0}:\n")
    for r in results:
        buf.write(f"{r['name']}: t={r['t']} P={r['p']}\n")

    buf.seek(0)
    return send_file(
        io.BytesIO(buf.getvalue().encode()),
        as_attachment=True,
        download_name='report.txt',
        mimetype='text/plain'
    )


if __name__ == '__main__':
    app.run(debug=True)