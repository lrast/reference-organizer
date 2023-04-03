# setup for graph QL interface
import graphene

import sqlalchemy as sa

from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import *



class TopicTopicEdgeType(SQLAlchemyObjectType):
    class Meta:
        model = TopicTopicAssociation

class PagePageEdgeType(SQLAlchemyObjectType):
    class Meta:
        model = PagePageAssociation


class PageType(SQLAlchemyObjectType):
    class Meta:
        model = Page

    rightEdges = graphene.List( PagePageEdgeType, relationshipid=graphene.Int(), remoteid=graphene.Int())
    leftEdges = graphene.List( PagePageEdgeType, relationshipid=graphene.Int(), remoteid=graphene.Int())

    def resolve_rightEdges(self, info, relationshipid=None, remoteid=None):
        query = PagePageEdgeType.get_query(info).filter(PagePageAssociation.leftpageid == self.id)

        if relationshipid is not None:
            query = query.filter( PagePageAssociation.relationshipid == relationshipid)
        if remoteid is not None:
            query = query.filter( PagePageAssociation.rightpageid == remoteid)

        return query.all()

    def resolve_leftEdges(self, info, relationshipid=None, remoteid=None):
        query = PagePageEdgeType.get_query(info).filter(PagePageAssociation.rightpageid == self.id)

        if relationshipid is not None:
            query = query.filter( PagePageAssociation.relationshipid == relationshipid)
        if remoteid is not None:
            query = query.filter( PagePageAssociation.leftpageid == remoteid)

        return query.all()



class TopicType(SQLAlchemyObjectType):
    class Meta:
        model = Topic

    rightEdges = graphene.List( TopicTopicEdgeType, relationshipid=graphene.Int(), remoteid=graphene.Int())
    leftEdges = graphene.List( TopicTopicEdgeType, relationshipid=graphene.Int(), remoteid=graphene.Int())

    def resolve_rightEdges(self, info, relationshipid=None, remoteid=None):
        query = TopicTopicEdgeType.get_query(info).filter(TopicTopicAssociation.lefttopicid == self.id)

        if relationshipid is not None:
            query = query.filter( TopicTopicAssociation.relationshipid == relationshipid)
        if remoteid is not None:
            query = query.filter( TopicTopicAssociation.righttopicid == remoteid)

        return query.all()

    def resolve_leftEdges(self, info, relationshipid=None, remoteid=None):
        query = TopicTopicEdgeType.get_query(info).filter(TopicTopicAssociation.righttopicid == self.id)

        if relationshipid is not None:
            query = query.filter( TopicTopicAssociation.relationshipid == relationshipid)
        if remoteid is not None:
            query = query.filter( TopicTopicAssociation.lefttopicid == remoteid)

        return query.all()



class RelationshipType(SQLAlchemyObjectType):
    class Meta:
        model = Relationship


class Query(graphene.ObjectType):
    topics = graphene.List(TopicType, id=graphene.Int(), name=graphene.String())
    pages = graphene.List(PageType, id=graphene.Int(), name=graphene.String())
    relationships = graphene.List(RelationshipType)

    def resolve_topics(self, info, id=None, name=None):
        query = TopicType.get_query(info)
        if id is not None:
            query = query.filter(Topic.id == id)
        if name is not None:
            query = query.filter(Topic.name == name)
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
        return None

    query_result = schema.execute(query)

    if query_result.errors is not None:
        print(query_result.errors)
        return query_result.errors[0].message, 400

    return jsonify( query_result.data )

