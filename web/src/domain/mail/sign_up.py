from uuid import UUID

from src.config.web import WEB_CONFIG


def build_sign_up_mail(user_id: UUID):
    accept_link = f'{WEB_CONFIG.url}/api/v1/auth/accept/{user_id}'

    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация на BookProject</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #4CAF50;
            font-size: 24px;
        }}
        p {{
            font-size: 16px;
            margin-bottom: 20px;
        }}
        a {{
            color: #4CAF50;
            text-decoration: none;
        }}
        button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>

    <div class="container">
        <h1>Вы прошли регистрацию на BookProject!</h1>
        <p>Чтобы подтвердить свою почту, перейдите по <a href="{accept_link}">ссылке</a> или нажмите на кнопку "Подтвердить".</p>
        <a href="{accept_link}">
            <button type="button">Подтвердить</button>
        </a>
    </div>

</body>
</html>
    """

    return html
