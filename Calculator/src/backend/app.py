# pyright: reportMissingImports=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUntypedFunctionDecorator=false

from typing import Any, Dict, Tuple, Union, cast

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate() -> Union[Tuple[Response, int], Response]:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON body'}), 400

    payload = cast(Dict[str, Any], data)

    a: Any = payload.get('a')
    b: Any = payload.get('b')
    op_raw: Any = payload.get('operator')

    if a is None or b is None or op_raw is None:
        return jsonify({'error': 'Missing values'}), 400

    try:
        a_num = float(a)
        b_num = float(b)
        op = str(op_raw)

        if op == '+':
            result = a_num + b_num
        elif op == '-':
            result = a_num - b_num
        elif op == '*':
            result = a_num * b_num
        elif op == '/':
            if b_num == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = a_num / b_num
        else:
            return jsonify({'error': 'Invalid operator'}), 400

        return jsonify({'result': result})
    except (TypeError, ValueError) as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)