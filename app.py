from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Разрешает запросы с других доменов

app = Flask(__name__)
CORS(app)  # Разрешаем кросс-доменные запросы

# Главная страница - показываем форму
@app.route('/')
def index():
    return render_template('signup.html')

# Обработка регистрации
@app.route('/register', methods=['POST'])
def register():
    try:
        # Получаем данные из формы
        data = request.form
        # или request.json если отправляете JSON
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Валидация на сервере
        if not username or len(username) < 3:
            return jsonify({
                'success': False,
                'error': 'Имя пользователя должно быть минимум 3 символа'
            }), 400
            
        if not email or '@' not in email:
            return jsonify({
                'success': False,
                'error': 'Введите корректный email'
            }), 400
            
        if not password or len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Пароль должен быть минимум 6 символов'
            }), 400
        
        # Здесь обычно сохранение в базу данных
        # Например, в SQLite, PostgreSQL и т.д.
        
        print(f"Новый пользователь: {username}, {email}, {password}")
        
        # Отправляем успешный ответ
        return jsonify({
            'success': True,
            'message': 'Регистрация успешна!',
            'user': {
                'username': username,
                'email': email
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=5000)