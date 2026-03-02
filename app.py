from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Разрешает запросы с других доменов
from database import register_user, login_user

app = Flask(__name__)
CORS(app)  # Разрешаем кросс-доменные запросы

# Главная страница - показываем форму
@app.route('/')
def index():
    return render_template('signup.html')

# Страница входа
@app.route('/signin')
def signin_page():
    return render_template('signin.html')

# Обработка регистрации
@app.route('/register', methods=['POST'])
def register():
    try:
        # Получаем данные из формы
        data = request.form
        
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
            
        if not password or len(password) < 8:
            return jsonify({
                'success': False,
                'error': 'Пароль должен быть минимум 8 символов'
            }), 400
        
        # Cохранение в базу данных
        
        result = register_user(username, email, password, "пусто")
        
        # Отправляем успешный ответ, в случае если регистрация успешна
        if result:
            return jsonify({
                'success': True,
                'message': 'Регистрация успешна!',
                'user': {
                    'username': username,
                    'email': email
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Этот email уже занят или произошла ошибка базы данных'
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




# Обработка входа
@app.route('/login', methods=['POST'])
def login():
    try:
        # Получаем данные из формы
        data = request.form
        
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember') == 'true'  # Преобразуем строку в boolean
        
        # Валидация на сервере
        if not email or '@' not in email:
            return jsonify({
                'success': False,
                'error': 'Введите корректный email'
            }), 400
            
        if not password:
            return jsonify({
                'success': False,
                'error': 'Введите пароль'
            }), 400
        
        # Пытаемся войти
        user_id = login_user(email, password)
        
        if user_id:
            # Успешный вход
            return jsonify({
                'success': True,
                'message': 'Вход выполнен успешно!',
                'user_id': user_id,
                'token': 'dummy-token-' + str(user_id)  # Простой токен для демо
            }), 200
        else:
            # Неудачный вход
            return jsonify({
                'success': False,
                'error': 'Неверный email или пароль'
            }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500







# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=5000)