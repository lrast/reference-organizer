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



