from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()

# Пример HTML страницы для регистрации
signup_html = """
<form action="/signup" method="post">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Sign Up</button>
</form>
"""

# Пример HTML страницы для логина
login_html = """
<form action="/login" method="post">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Log In</button>
</form>
"""

# Путь к JSON-файлу
data_file = "users.json"

# Проверяем, существует ли файл, если нет, создаем его
if not os.path.exists(data_file):
    with open(data_file, "w") as file:
        json.dump({}, file)

@app.get("/signup", response_class=HTMLResponse)
async def signup_form():
    return signup_html

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    # Загружаем данные из JSON-файла
    with open(data_file, "r") as file:
        users = json.load(file)

    if username in users:
        return "Username already exists. Please choose a different username."

    # Добавляем нового пользователя
    users[username] = {"password": password}

    # Сохраняем обновленные данные в JSON-файл
    with open(data_file, "w") as file:
        json.dump(users, file)

    return "Registration successful!"

@app.get("/login", response_class=HTMLResponse)
async def login_form():
    return login_html

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Загружаем данные из JSON-файла
    with open(data_file, "r") as file:
        users = json.load(file)

    if username not in users or users[username]["password"] != password:
        return "Invalid username or password."

    return "Login successful!"

@app.get("/get_users")
async def get_users():
    # Загружаем данные из JSON-файла
    with open(data_file, "r") as file:
        users = json.load(file)
    return users

