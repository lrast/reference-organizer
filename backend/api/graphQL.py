# setup for graph QL interface
import sqlalchemy as sa
from sqlalchemy.orm import aliased

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from database.model import *

from flask import Blueprint, request, jsonify


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

    allSubTopics = graphene.List(lambda: TopicType)


    def resolve_allSubTopics(self, info):
        from backend import sqlaDB as db

        topicAlias = aliased(Topic)

        subtopicsQuery = db.session.query(Topic.id).filter(Topic.id==self.id).cte(name='subtopicsQuery', recursive=True)
        subtopicsQuery = subtopicsQuery.union( db.session.query(topicAlias.id).join(subtopicsQuery, topicAlias.rightTopics) )

        subtopicIds = map( lambda x: x[0], db.session.query(subtopicsQuery).all() )

        grapheneQuery = TopicType.get_query(info).filter( Topic.id.in_(subtopicIds) )

        return grapheneQuery.all()


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
    topics = graphene.List(TopicType, id=graphene.Int(), name=graphene.String(), ids=graphene.List(graphene.Int) )
    pages = graphene.List(PageType, id=graphene.Int(), name=graphene.String(), ids=graphene.List(graphene.Int) )
    relationships = graphene.List(RelationshipType)

    def resolve_topics(self, info, id=None, name=None, ids=[]):
        query = TopicType.get_query(info)

        if id is not None:
            query = query.filter(Topic.id == id)
        elif len(ids) != 0:
            query = query.filter( Topic.id.in_(ids) )
        if name is not None:
            query = query.filter(Topic.name == name)
        return query.all()

    def resolve_pages(self, info, id=None, name=None, ids=[]):
        query = PageType.get_query(info)
        if id is not None:
            query = query.filter(Page.id == id)
        elif len(ids) != 0:
            query = query.filter(Page.id.in_(ids) )
        if name is not None:
            query = query.filter(Page.name == name)
        return query.all()

    def resolve_relationships(self, info):
        query = RelationshipType.get_query(info)
        return query.all()



########################################### Utilities ###########################################

schema = graphene.Schema(query=Query)

def execute_gql_query(query, unpackage=lambda x:x):
    """ run the query. unpackage is a function on the result """
    query_result = schema.execute(query)

    if query_result.errors is not None:
        return query_result.errors[0].message, 400

    return unpackage( query_result.data )


# endpoint
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
