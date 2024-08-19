def get_index_html(pico_info, esp_info, weather_info):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IOT Control Panel</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-image: url('https://pic.616pic.com/bg_w1180/00/00/99/1uH88ZEgMH.jpg'); /* 替换为您选择的背景图像 */
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.9); /* 半透明背景 */
                border-radius: 15px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
                padding: 20px;
                max-width: 800px;
                width: 90%;
                margin: 20px;
                box-sizing: border-box;
                backdrop-filter: blur(10px); /* 背景模糊效果 */
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 15px;
                font-size: 2.5em;
                text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
            }}
            .module {{
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: #f9f9f9;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .module:hover {{
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            }}
            .module h2 {{
                color: #555;
                margin-bottom: 10px;
                font-size: 1.5em;
            }}
            .info {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
                font-size: 1.1em;
                color: #333;
            }}
            .nav {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 15px;
                width: 100%;
            }}
            .nav a {{
                text-decoration: none;
                color: #007bff;
                padding: 10px 15px;
                border-radius: 5px;
                transition: background-color 0.3s;
            }}
            .nav a:hover {{
                background-color: #e7f0ff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>IOT Control Panel</h1>
            <div class="nav">
                <a href="/">首页</a>
                <a href="/dev_ctl">设备控制</a>
                <a href="/setting">设置</a>
            </div>
            <div class="module">
                <h2>Pico 信息</h2>
                <div class="info"><strong>设备型号:</strong> <span>{pico_info['model']}</span></div>
                <div class="info"><strong>MicroPython 版本:</strong> <span>{pico_info['micropython_version']}</span></div>
                <div class="info"><strong>CPU 频率:</strong> <span>{pico_info['cpu_frequency']} MHz</span></div>
                <div class="info"><strong>内存大小:</strong> <span>{pico_info['memory_size']} KB</span></div>
                <div class="info"><strong>温度:</strong> <span>{pico_info['temperature']} °C</span></div>
            </div>
            <div class="module">
                <h2>ESP8266 信息</h2>
                <div class="info"><strong>固件信息:</strong> <span>{esp_info['firmware']}</span></div>
                <div class="info"><strong>可用内存:</strong> <span>{esp_info['free_memory']} KB</span></div>
                <div class="info"><strong>温度:</strong> <span>{esp_info['temperature']} °C</span></div>
            </div>
            <div class="module">
                <h2>天气信息</h2>
                <div class="info"><strong>温度:</strong> <span>{weather_info['temperature']} °C</span></div>
                <div class="info"><strong>湿度:</strong> <span>{weather_info['humidity']} %</span></div>
                <div class="info"><strong>天气状况:</strong> <span>{weather_info['condition']}</span></div>
            </div>
        </div>
    </body>
    </html>
    """