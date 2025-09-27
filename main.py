from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import base64
import qrcode
import io

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <title>QR Generator</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Генератор QR-кодов</h2>
            <form action="/generate" method="post">
                <input type="text" name="url" placeholder="Введите ссылку" size="40" required>
                <button type="submit">Создать QR</button>
            </form>
        </body>
    </html>
    """


@app.post("/generate", response_class=HTMLResponse)
def generate_qrcode(url: str = Form(...)):
    # Генерация QR-кода
    qr = qrcode.make(url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    img_str = base64.b64encode(img_bytes).decode()

    # Возвращаем HTML с картинкой и кнопкой скачивания
    return f"""
    <html>
        <head>
            <title>QR Result</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Ваш QR-код</h2>
            <img src="data:image/png;base64,{img_str}" alt="QR Code">
            <br><br>
            <a href="data:image/png;base64,{img_str}" download="qrcode.png">
                <button>Скачать QR-код</button>
            </a>
            <br><br>
            <a href="/">Назад</a>
        </body>
    </html>
    """