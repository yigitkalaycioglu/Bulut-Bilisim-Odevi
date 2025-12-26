from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def hello_cloud():
    host_name = socket.gethostname()
    return f"""
    <h1>Bulut Bilisim Odevi - Merhaba!</h1>
    <p>Bu uygulama AWS EC2 uzerinde calismaktadir.</p>
    <p>Sunucu ID/Host: <b>{host_name}</b></p>
    """

if __name__ == '__main__':
    # 0.0.0.0 diyerek dıs dunyaya aciyoruz
    app.run(host='0.0.0.0', port=5000)