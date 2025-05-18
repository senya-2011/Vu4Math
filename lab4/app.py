from flask import Flask, render_template, request, flash, redirect, session, url_for, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
import methodology.point_5
from file_reader import read_xy_from_txt_filepath
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.template_filter('zip')
def zip_filter(a, b, c):
    return zip(a, b, c)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            x_test, y_test = [], []
            use_file = False

            # Обработка файла
            if 'data_file' in request.files:
                file = request.files['data_file']
                if file.filename != '':
                    if not file.filename.lower().endswith('.txt'):
                        flash('Ошибка: Недопустимый тип файла')
                        return redirect(url_for('index'))

                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                    file.save(file_path)

                    try:
                        x_test, y_test = read_xy_from_txt_filepath(file_path)
                        use_file = True
                    except Exception as e:
                        flash(f'Ошибка файла: {str(e)}')
                        return redirect(url_for('index'))
                    finally:
                        if os.path.exists(file_path):
                            os.remove(file_path)

            # Если файл не использован, проверяем поля ввода
            if not use_file:
                x_input = request.form.get('x_values', '').replace(',', '.').strip()
                y_input = request.form.get('y_values', '').replace(',', '.').strip()

                # Проверка на полную пустоту
                if not x_input and not y_input:
                    flash('Ошибка: Необходимо либо загрузить файл, либо ввести данные в поля')
                    return redirect(url_for('index'))

                # Проверка что заполнены оба поля
                if not x_input or not y_input:
                    flash('Ошибка: Необходимо заполнить оба поля (X и Y)')
                    return redirect(url_for('index'))

                try:
                    x_test = list(map(float, x_input.split()))
                    y_test = list(map(float, y_input.split()))
                except ValueError:
                    flash('Ошибка: Некорректные числовые значения в полях ввода')
                    return redirect(url_for('index'))

            # Проверка что данные вообще есть
            if not x_test or not y_test:
                flash('Ошибка: Нет данных для анализа')
                return redirect(url_for('index'))


            if len(x_test) != len(y_test):
                flash('Ошибка: Количество значений X и Y должно совпадать')
                return redirect(url_for('index'))

            if any(x <= 0 for x in x_test):
                flash('Ошибка: Все значения X должны быть больше 0')
                return redirect(url_for('index'))

            if not (8 <= len(x_test) <= 12):
                flash('Ошибка: Требуется от 8 до 12 значений в каждой строке')
                return redirect(url_for('index'))

            # Сохраняем данные в сессии
            session['x_test'] = x_test
            session['y_test'] = y_test

            # Остальная логика обработки...
            result = methodology.point_5.run_full_pipeline(x_test, y_test)

            models_data = []
            for model_result in result['results']:
                model_name = model_result['name']
                predictions = next(p[2] for p in result['predictions'] if p[0] == model_name)
                stats = next(s for s in result['stats'] if s['name'] == model_name)

                models_data.append({
                    'name': model_name,
                    'coeffs': model_result['coeffs'],
                    'mse': model_result['mse'],
                    'stats': stats,
                    'predictions': predictions
                })

            return render_template(
                'results.html',
                models_data=models_data,
                result=result,
                x_test=x_test,
                y_test=y_test,
                best_model=result['best']['name']
            )

        except Exception as e:
            flash(f'Ошибка: {str(e)}')
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/download-report')
def download_report():
    try:
        # Получаем данные из сессии
        x_test = session.get('x_test', [])
        y_test = session.get('y_test', [])

        if not x_test or not y_test:
            flash('Нет данных для отчета')
            return redirect(url_for('index'))

        result = methodology.point_5.run_full_pipeline(x_test, y_test)

        # Генерация отчета...
        report = [f"Лучшая модель: {result['best']['name']}\n"]

        for model in result['results']:
            report.append(f"\nМодель: {model['name']}")
            report.append(f"Коэффициенты: {model['coeffs']}")
            report.append(f"MSE: {model['mse']:.2e}")

            predictions = next(p[2] for p in result['predictions'] if p[0] == model['name'])
            report.append("\nТаблица данных:")
            report.append("X\t\tY\t\tY_pred\t\tОшибка")
            for x, y, y_pred in zip(x_test, y_test, predictions):
                error = y - y_pred
                report.append(f"{x:.4f}\t\t{y:.4f}\t\t{y_pred:.4f}\t\t{error:.4f}")

        buffer = BytesIO()
        buffer.write('\n'.join(report).encode('utf-8'))
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name='report.txt',
            mimetype='text/plain'
        )

    except Exception as e:
        flash(f'Ошибка генерации отчета: {str(e)}')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)