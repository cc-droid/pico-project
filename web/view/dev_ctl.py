def get_dev_ctl_html(state, random_value):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Device Control</title>
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
            .status {{
                font-weight: bold;
                color: #333;
            }}
            p {{
                text-align: center;
                font-size: 16px;
                color: #333;
            }}
            form {{
                display: flex;
                justify-content: center;
                margin-bottom: 10px;
            }}
            input[type="submit"] {{
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s ease;
                width: 100%;
            }}
            input[type="submit"]:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Device Control</h1>
            <div class="section">
                <h2>LED Control</h2>
                <form action="/lighton">
                    <input type="submit" value="Turn Light On" />
                </form>
                <form action="/lightoff">
                    <input type="submit" value="Turn Light Off" />
                </form>
                <p>LED State: <span class="status">{state}</span></p>
            </div>
            <div class="section">
                <h2>Fetch Random Value</h2>
                <form action="/value">
                    <input type="submit" value="Fetch Value" />
                </form>
                <p>Fetched Value: <span class="status">{random_value}</span></p>
            </div>
        </div>
    </body>
    </html>
    """