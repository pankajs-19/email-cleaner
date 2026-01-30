from flask import Flask, jsonify, request, render_template
from loguru import logger
from connector_component import list_mail_messages, get_mail_body
from auth_mgmt import AuthMgmt

auth_manager = AuthMgmt()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-mails', methods=['GET'])
def get_all_mails():
    try:
        logger.info("API call to /api/get-mails")
        batch_size = request.args.get('batch_size', type=int, default=10)
        from_date = request.args.get('from_date', None)
        end_date = request.args.get('end_date', None)
        credentials = auth_manager.get_credentials()
        mails = list_mail_messages(credentials, from_date=from_date, end_date=end_date, batch_size=batch_size)
        return jsonify({"data": mails}), 200
    except Exception as e:
        logger.error(f"Error in get-mails endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-body', methods=['GET'])
def get_body():
    try:
        logger.info("API call to get body invoked")
        msg_id = request.args.get("message_id", None)
        if not msg_id:
            return jsonify({'error': 'message_id parameter is required'}), 400
        
        credentials = auth_manager.get_credentials()
        message_body = get_mail_body(credentials, msg_id)
        if not message_body:
            logger.error("could not message body")
            return jsonify({"error": "could not message body"}), 500
        
        return jsonify(message_body), 200
        
    except Exception as e:
        logger.error(f"error fetching message body: {e}")
        return jsonify({"error":f"error fetching message body - {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True) 