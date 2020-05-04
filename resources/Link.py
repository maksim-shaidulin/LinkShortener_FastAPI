from flask import request
from flask_restful import Resource
# from Model import db, Category, CategorySchema
from Model import db, Link, LinkSchema
from marshmallow import ValidationError
from typing import Tuple

links_schema = LinkSchema(many=True)
link_schema = LinkSchema()


class LinkListResource(Resource):
    def get(self):
        links = Link.query.all()
        if links:
            links = links_schema.dump(links)
        return {'status': 'success', 'data': links}, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = link_schema.load(json_data)
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)
            return err.messages, 422
        except ValueError as err:
            print(err)
            return str(err), 422

        link = Link.query.filter_by(full_link=data['full_link']).first()
        if link:
            print(f'{link.full_link} already exists')
            return {'status': 'success', 'data': link.short_link}, 201

        link = Link(json_data['full_link'])

        db.session.add(link)
        db.session.commit()

        return {"status": 'success', 'data': link.short_link}, 201


class LinkResource(Resource):
    def get(self, short_link: str) -> Tuple:
        link = Link.query.filter_by(short_link=short_link).first()
        if link:
            link = link_schema.dump(link)
            return {'status': 'success', 'data': link}, 204
        else:
            return {'status': 'error',
                    'message': f'Link {short_link} does not exist'}, 404

    def delete(self, short_link: str):
        link = Link.query.filter_by(short_link=short_link).first()
        if link:
            Link.query.filter_by(short_link=short_link).delete()
            db.session.commit()
            return {"status": 'success',
                    'message': f'Link {short_link} is deleted'}, 204
        else:
            return {'status': 'error',
                    'message': f'Link {short_link} does not exist'}, 404
