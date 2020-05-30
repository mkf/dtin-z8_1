from flask import Flask, request, abort, jsonify
from jsonschema import validate, ValidationError

POSITIVE_INTEGER_SCHEMA = {
    "type": "integer",
    "exclusiveMinimum": 0
}

def object_schema(*properties):
    return {
        "type": "object",
        "properties": {key: POSITIVE_INTEGER_SCHEMA for key in properties},
        "additionalProperties": False,
        "requiredProperties": properties
    }

INPUT_SCHEMA = object_schema("token", "a", "b")

OUTPUT_SCHEMA = object_schema("token", "product")

validate(instance={
  "token": 1234567890,
  "a": 4718923648912376,
  "b": 4710943190713794
}, schema=INPUT_SCHEMA)

app = Flask(__name__)

@app.route('/product', methods=['POST'])
def product():
    json = request.get_json(force=True) # no need for Content-Type header
    # we discard the mimetype because the task suggested using curl with just
    # the -d parameter and without -H Content-Type application/json
    # If the data is not valid json, werkzeug does 400 as well.

    if not json:
        abort(400)
    # because why not. that might be redundant tho.

    try:
        validate(instance=json, schema=INPUT_SCHEMA)
    except ValidationError as e:
        print("invalid: ", e)
        abort(400)
    else:
        token, a, b = (json[k] for k in ("token", "a", "b"))
        r = {"token": token, "product": a*b}
        validate(instance=r, schema=OUTPUT_SCHEMA)
        return jsonify(r)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 6543, app)
    server.serve_forever()
