from flask import Flask, jsonify, request, render_template
from loguru import logger
from connector_component import get_mails

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-mails', methods=['GET'])
def get_all_mails():
    try:
        logger.info("API call to /api/get-mails")
        batch_size = request.args.get('batch_size', 10)
        from_date = request.args.get('from_date', None)
        end_date = request.args.get('to_date', None)
        mails = get_mails(from_date, end_date, batch_size)
        return jsonify(mails), 200
    except Exception as e:
        logger.error(f"Error in /api/get-mails endpoint: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True) 