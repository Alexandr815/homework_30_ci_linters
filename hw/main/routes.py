from flask import request, jsonify
from app import db
from models import Client, Parking, ClientParking
from datetime import datetime


def register_routes(app):

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = Client.query.all()
        return jsonify([c.id for c in clients]), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify({"id": client.id, "name": client.name}), 200

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.json
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
        return jsonify({"id": client.id}), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.json
        parking = Parking(**data)
        db.session.add(parking)
        db.session.commit()
        return jsonify({"id": parking.id}), 201

    @app.route("/client_parkings", methods=["POST"])
    def enter_parking():
        data = request.json

        client = Client.query.get(data["client_id"])
        parking = Parking.query.get(data["parking_id"])

        if not parking.opened or parking.count_available_places <= 0:
            return {"error": "No places"}, 400

        parking.count_available_places -= 1

        cp = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.utcnow()
        )

        db.session.add(cp)
        db.session.commit()

        return {"message": "entered"}, 200

    @app.route("/client_parkings", methods=["DELETE"])
    def exit_parking():
        data = request.json

        cp = ClientParking.query.filter_by(
            client_id=data["client_id"],
            parking_id=data["parking_id"]
        ).first()

        client = Client.query.get(data["client_id"])
        parking = Parking.query.get(data["parking_id"])

        if not client.credit_card:
            return {"error": "No card"}, 400

        cp.time_out = datetime.utcnow()
        parking.count_available_places += 1

        db.session.commit()

        return {"message": "exited"}, 200