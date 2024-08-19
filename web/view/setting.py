def get_setting_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}
            .container {{
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 600px;
                width: 90%;
                margin: 20px;
                box-sizing: border-box;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Settings</h1>
            <p>Settings page content goes here.</p>
        </div>
    </body>
    </html>
    """