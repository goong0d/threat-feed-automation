from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔼 PUSH Routes
@app.route('/api/ip_push', methods=['POST'])
def ip_push():
    data = request.get_json()
    if not data or 'ip' not in data:
        return jsonify({"status": "error", "message": "Invalid IP data"}), 400
    print("🔥 [IP PUSH] →", data['ip'])
    return jsonify({"status": "IP received"}), 200

@app.route('/api/domain_push', methods=['POST'])
def domain_push():
    data = request.get_json()
    if not data or 'domain' not in data:
        return jsonify({"status": "error", "message": "Invalid domain data"}), 400
    print("🌐 [DOMAIN PUSH] →", data['domain'])
    return jsonify({"status": "Domain received"}), 200

@app.route('/api/hash_push', methods=['POST'])
def hash_push():
    data = request.get_json()
    if not data or 'hash' not in data:
        return jsonify({"status": "error", "message": "Invalid hash data"}), 400
    print("🔒 [HASH PUSH] →", data['hash'])
    return jsonify({"status": "Hash received"}), 200

# 🔽 DELETE Routes
@app.route('/api/ip_delete', methods=['POST'])
def ip_delete():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"status": "error", "message": "Invalid delete IP data"}), 400
    print("🗑️ [IP DELETE] →", data['value'])
    return jsonify({"status": "IP deleted"}), 200

@app.route('/api/domain_delete', methods=['POST'])
def domain_delete():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"status": "error", "message": "Invalid delete domain data"}), 400
    print("🗑️ [DOMAIN DELETE] →", data['value'])
    return jsonify({"status": "Domain deleted"}), 200

@app.route('/api/hash_delete', methods=['POST'])
def hash_delete():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"status": "error", "message": "Invalid delete hash data"}), 400
    print("🗑️ [HASH DELETE] →", data['value'])
    return jsonify({"status": "Hash deleted"}), 200

# 🔧 Server config
if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
