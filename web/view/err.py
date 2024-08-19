def get_404_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 Not Found</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            .container {
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 600px;
                width: 90%;
                text-align: center;
            }
            h1 {
                color: #d9534f; /* Bootstrap danger color */
            }
            p {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404 Not Found</h1>
            <p>抱歉，您请求的页面未找到。</p>
            <p><a href="/">返回首页</a></p>
        </div>
    </body>
    </html>
    """