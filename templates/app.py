from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/health')
def health():
    return render_template('health.html')

# Add more routes as needed

if __name__ == '__main__':
    app.run(debug=True)