# setup for graph QL interface
import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import Page, Topic, Relationship


class PageType(SQLAlchemyObjectType):
    class Meta:
        model = Page

class TopicType(SQLAlchemyObjectType):
    class Meta:
        model = Topic

class RelationshipType(SQLAlchemyObjectType):
    class Meta:
        model = Relationship


class Query(graphene.ObjectType):
    topics = graphene.List(TopicType)
    pages = graphene.List(PageType)
    relationships = graphene.List(RelationshipType)


    def resolve_topics(self, info):
        query = TopicType.get_query(info)
        return query.all()

    def resolve_pages(self, info):
        query = PageType.get_query(info)
        return query.all()

    def resolve_relationships(self, info):
        query = RelationshipType.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query)



# endpoint
import json
from flask import Blueprint, request, Response, jsonify

GQLendpoint = Blueprint('gql', __name__)

@GQLendpoint.route('/', methods=['GET'])
def acceptQuery():
    query = request.args.get('query', None)
    if not query:
        return '{}'

    print(schema.execute(query))

    return jsonify( schema.execute(query).data )

