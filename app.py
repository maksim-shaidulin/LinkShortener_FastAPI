from flask import Blueprint
from flask_restful import Api

from resources.Hello import Hello
# from resources.Category import CategoryResource
# from resources.Comment import CommentResource
from resources.Link import LinkListResource, LinkResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/hello')
api.add_resource(LinkListResource, '/link')
api.add_resource(LinkResource, '/link/<short_link>')
# api.add_resource(CategoryResource, '/Category')
# api.add_resource(CommentResource, '/Comment')
