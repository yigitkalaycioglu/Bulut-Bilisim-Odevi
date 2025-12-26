from flask import Flask
import socket

app = Flask(__name__)


@app.route('/')
def index():
    # Sunucu ismini (Instance ID) alalim ki bulutta oldugu belli olsun
    host_name = socket.gethostname()

    # HTML, CSS ve JavaScript kodunu tek string icine gomuyoruz
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AWS Cloud Pong</title>
        <style>
            body {{
                background-color: #1a1a1a;
                color: #ecf0f1;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{ margin-bottom: 5px; text-shadow: 0 0 10px #00ff00; }}
            .server-info {{
                color: #aaa;
                font-size: 14px;
                margin-bottom: 20px;
                border: 1px solid #333;
                padding: 5px 15px;
                border-radius: 20px;
                background: #222;
            }}
            canvas {{
                border: 4px solid #fff;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
                background: black;
                cursor: none; /* Oyun alaninda mouse gizlensin */
            }}
            .controls {{ margin-top: 15px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>

        <h1>AWS BULUT PONG</h1>
        <div class="server-info">Sunucu ID: <b>{host_name}</b> | Port: 5000</div>

        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div class="controls">Kontrol: Mouse'u yukarı aşağı hareket ettirin</div>

        <script>
            var canvas;
            var canvasContext;

            // Top degiskenleri
            var ballX = 50;
            var ballY = 50;
            var ballSpeedX = 10;
            var ballSpeedY = 4;

            // Skorlar
            var player1Score = 0;
            var player2Score = 0;
            const WINNING_SCORE = 5;

            var showingWinScreen = false;

            // Raketler
            var paddle1Y = 250;
            var paddle2Y = 250;
            const PADDLE_THICKNESS = 10;
            const PADDLE_HEIGHT = 100;

            window.onload = function() {{
                canvas = document.getElementById('gameCanvas');
                canvasContext = canvas.getContext('2d');

                var framesPerSecond = 30;
                setInterval(function() {{
                    moveEverything();
                    drawEverything();
                }}, 1000/framesPerSecond);

                canvas.addEventListener('mousedown', handleMouseClick);

                canvas.addEventListener('mousemove',
                    function(evt) {{
                        var mousePos = calculateMousePos(evt);
                        paddle1Y = mousePos.y - (PADDLE_HEIGHT/2);
                    }});
            }};

            function handleMouseClick(evt) {{
                if(showingWinScreen) {{
                    player1Score = 0;
                    player2Score = 0;
                    showingWinScreen = false;
                }}
            }}

            function calculateMousePos(evt) {{
                var rect = canvas.getBoundingClientRect();
                var root = document.documentElement;
                var mouseX = evt.clientX - rect.left - root.scrollLeft;
                var mouseY = evt.clientY - rect.top - root.scrollTop;
                return {{
                    x:mouseX,
                    y:mouseY
                }};
            }}

            function ballReset() {{
                if(player1Score >= WINNING_SCORE || player2Score >= WINNING_SCORE) {{
                    showingWinScreen = true;
                }}
                ballSpeedX = -ballSpeedX;
                ballX = canvas.width/2;
                ballY = canvas.height/2;
            }}

            function computerMovement() {{
                var paddle2YCenter = paddle2Y + (PADDLE_HEIGHT/2);
                if(paddle2YCenter < ballY - 35) {{
                    paddle2Y += 6;
                }} else if(paddle2YCenter > ballY + 35) {{
                    paddle2Y -= 6;
                }}
            }}

            function moveEverything() {{
                if(showingWinScreen) {{
                    return;
                }}

                computerMovement();

                ballX += ballSpeedX;
                ballY += ballSpeedY;

                // Sol taraf (Oyuncu)
                if(ballX < 0) {{
                    if(ballY > paddle1Y && ballY < paddle1Y+PADDLE_HEIGHT) {{
                        ballSpeedX = -ballSpeedX;
                        // Topa egim ver
                        var deltaY = ballY - (paddle1Y+PADDLE_HEIGHT/2);
                        ballSpeedY = deltaY * 0.35;
                    }} else {{
                        player2Score++; // Bilgisayar puani
                        ballReset();
                    }}
                }}

                // Sag taraf (Bilgisayar)
                if(ballX > canvas.width) {{
                    if(ballY > paddle2Y && ballY < paddle2Y+PADDLE_HEIGHT) {{
                        ballSpeedX = -ballSpeedX;
                        var deltaY = ballY - (paddle2Y+PADDLE_HEIGHT/2);
                        ballSpeedY = deltaY * 0.35;
                    }} else {{
                        player1Score++; // Oyuncu puani
                        ballReset();
                    }}
                }}

                // Yukari ve asagi duvarlar
                if(ballY < 0) {{ ballSpeedY = -ballSpeedY; }}
                if(ballY > canvas.height) {{ ballSpeedY = -ballSpeedY; }}
            }}

            function drawNet() {{
                for(var i=0; i<canvas.height; i+=40) {{
                    colorRect(canvas.width/2-1,i,2,20,'white');
                }}
            }}

            function drawEverything() {{
                // Arkaplan
                colorRect(0,0,canvas.width,canvas.height,'black');

                if(showingWinScreen) {{
                    canvasContext.fillStyle = 'white';
                    canvasContext.font = "30px Courier New";

                    if(player1Score >= WINNING_SCORE) {{
                        canvasContext.fillText("TEBRIKLER! KAZANDINIZ!", 220, 200);
                    }} else if(player2Score >= WINNING_SCORE) {{
                        canvasContext.fillText("BILGISAYAR KAZANDI...", 230, 200);
                    }}

                    canvasContext.font = "20px Courier New";
                    canvasContext.fillText("Yeniden oynamak icin tiklayin", 250, 500);
                    return;
                }}

                drawNet();

                // Sol raket (Oyuncu)
                colorRect(0,paddle1Y,PADDLE_THICKNESS,PADDLE_HEIGHT,'#00ff00');

                // Sag raket (Bilgisayar)
                colorRect(canvas.width-PADDLE_THICKNESS,paddle2Y,PADDLE_THICKNESS,PADDLE_HEIGHT,'red');

                // Top
                colorCircle(ballX, ballY, 10, 'white');

                // Skorlar
                canvasContext.fillStyle = 'white';
                canvasContext.font = "50px Courier New";
                canvasContext.fillText(player1Score, 100, 100);
                canvasContext.fillText(player2Score, canvas.width-130, 100);
            }}

            function colorCircle(centerX, centerY, radius, drawColor) {{
                canvasContext.fillStyle = drawColor;
                canvasContext.beginPath();
                canvasContext.arc(centerX, centerY, radius, 0,Math.PI*2,true);
                canvasContext.fill();
            }}

            function colorRect(leftX,topY, width,height, drawColor) {{
                canvasContext.fillStyle = drawColor;
                canvasContext.fillRect(leftX,topY, width,height);
            }}
        </script>
    </body>
    </html>
    """
    return html_content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)