from flask import Flask, jsonify, request, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

properties = []
next_id = 1

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """
    Получить список всех объектов недвижимости
    ---
    responses:
      200:
        description: Список всех объектов недвижимости
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              address:
                type: string
                example: "ул. Ленина, д. 1"
              price:
                type: number
                format: float
                example: 5000000.00
              status:
                type: string
                example: "available"
              description:
                type: string
                example: "Прекрасная квартира в центре города"
    """
    return jsonify(properties)

@app.route('/api/properties', methods=['POST'])
def create_property():
    """
    Добавить новый объект недвижимости
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            address:
              type: string
              example: "ул. Ленина, д. 1"
            price:
              type: number
              format: float
              example: 5000000.00
            status:
              type: string
              example: "available"
            description:
              type: string
              example: "Прекрасная квартира в центре города"
    responses:
      201:
        description: Новый объект недвижимости добавлен
        schema:
          type: object
          properties:
            id:
              type: integer
            address:
              type: string
            price:
              type: number
              format: float
            status:
              type: string
            description:
              type: string
    """
    global next_id
    if not request.json or 'address' not in request.json or 'price' not in request.json:
        abort(400)
    property_item = {
        'id': next_id,
        'address': request.json['address'],
        'price': request.json['price'],
        'status': request.json.get('status', 'available'),
        'description': request.json.get('description', '')
    }
    next_id += 1
    properties.append(property_item)
    return jsonify(property_item), 201

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """
    Получить информацию об объекте недвижимости по ID
    ---
    parameters:
      - name: property_id
        in: path
        required: true
        type: integer
        description: ID объекта недвижимости
    responses:
      200:
        description: Информация об объекте недвижимости
        schema:
          type: object
          properties:
            id:
              type: integer
            address:
              type: string
            price:
              type: number
              format: float
            status:
              type: string
            description:
              type: string
      404:
        description: Объект недвижимости не найден
    """
    property_item = next((p for p in properties if p['id'] == property_id), None)
    if property_item is None:
        abort(404)
    return jsonify(property_item)

@app.route('/api/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    """
    Обновить информацию об объекте недвижимости по ID
    ---
    parameters:
      - name: property_id
        in: path
        required: true
        type: integer
        description: ID объекта недвижимости для обновления
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            address:
              type: string
              example: "ул. Ленина, д. 1"
            price:
              type: number
              format: float
              example: 5500000.00
            status:
              type: string
              example: "sold"
            description:
              type: string
              example: "Продано"
    responses:
      200:
        description: Информация об объекте недвижимости обновлена
        schema:
          type: object
          properties:
            id:
              type: integer
            address:
              type: string
            price:
              type: number
              format: float
            status:
              type: string
            description:
              type: string
      404:
        description: Объект недвижимости не найден
    """
    property_item = next((p for p in properties if p['id'] == property_id), None)
    if property_item is None:
        abort(404)
    if not request.json:
        abort(400)
    property_item['address'] = request.json.get('address', property_item['address'])
    property_item['price'] = request.json.get('price', property_item['price'])
    property_item['status'] = request.json.get('status', property_item['status'])
    property_item['description'] = request.json.get('description', property_item['description'])
    return jsonify(property_item)

@app.route('/api/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    """
    Удалить объект недвижимости по ID
    ---
    parameters:
      - name: property_id
        in: path
        required: true
        type: integer
        description: ID объекта недвижимости для удаления
    responses:
      200:
        description: Объект недвижимости удален
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
      404:
        description: Объект недвижимости не найден
    """
    global properties
    property_item = next((p for p in properties if p['id'] == property_id), None)
    if property_item is None:
        abort(404)
    properties = [p for p in properties if p['id'] != property_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
