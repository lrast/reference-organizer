# ORM data model
import sqlalchemy as sa
import sqlalchemy.orm as orm

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#association tables
PageTopicAssociation = db.Table(
    'PageTopic',
    sa.Column('id', sa.Integer, primary_key=True), 
    sa.Column('pageid', sa.Integer, sa.ForeignKey('Page.id')),
    sa.Column( 'topicid', sa.Integer, sa.ForeignKey('Topic.id'))
)

TopicTopicAssociation = db.Table(
    'TopicTopicRelationship',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('relationshipid', sa.Integer, sa.ForeignKey('Relationship.id')),
    sa.Column('lefttopicid', sa.Integer, sa.ForeignKey('Topic.id')),
    sa.Column('righttopicid', sa.Integer, sa.ForeignKey('Topic.id'))
)

PagePageAssociation =db.Table(
    'PagePageRelationship',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('relationshipid', sa.Integer, sa.ForeignKey('Relationship.id')),
    sa.Column('leftpageid', sa.Integer, sa.ForeignKey('Page.id')),
    sa.Column('rightpageid', sa.Integer, sa.ForeignKey('Page.id'))
)




# primary data model
class Page(db.Model):
    __tablename__ = 'Page'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column( sa.String, unique=True, nullable=False)
    name = sa.Column( sa.String )
    dateadded = sa.Column( sa.Date )

    topics = orm.relationship('Topic', secondary=PageTopicAssociation, back_populates='pages')
    related_pages_right = orm.relationship(
            'Page',
            secondary=PagePageAssociation,
            primaryjoin=(PagePageAssociation.c.leftpageid == id),
            secondaryjoin=(PagePageAssociation.c.rightpageid == id),
            backref='related_pages_left'
        )
    comments = orm.relationship('PageComments', back_populates='page')


class Topic(db.Model):
    __tablename__ = 'Topic'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    pages = orm.relationship('Page', secondary=PageTopicAssociation, back_populates='topics')
    related_topics_right = orm.relationship(
            'Topic',
            secondary=TopicTopicAssociation,
            primaryjoin=(TopicTopicAssociation.c.lefttopicid == id),
            secondaryjoin=(TopicTopicAssociation.c.righttopicid == id),
            backref='related_topics_left'
        )
    comments = orm.relationship('TopicComments', back_populates='topic')


class Relationship(db.Model):
    __tablename__ = 'Relationship'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    nodetype = sa.Column(sa.String, nullable=False)
    reversename = sa.Column(sa.String, nullable=False)

    comments = orm.relationship('RelationshipComments', back_populates='relationship')




# comments tables
class PageComments(db.Model):
    __tablename__ = 'PageComments'

    id = sa.Column(sa.Integer, primary_key=True)
    pageid = sa.Column(sa.Integer, sa.ForeignKey('Page.id'))
    dateadded = sa.Column(sa.Date)
    commentdata = sa.Column(sa.LargeBinary)

    page = orm.relationship('Page', back_populates='comments')


class TopicComments(db.Model):
    __tablename__ = 'TopicComments'

    id = sa.Column(sa.Integer, primary_key=True)
    topicid = sa.Column(sa.Integer, sa.ForeignKey('Topic.id'))
    dateadded = sa.Column(sa.Date)
    commentdata = sa.Column(sa.LargeBinary)

    topic = orm.relationship('Topic', back_populates='comments')


class RelationshipComments(db.Model):
    __tablename__ = 'RelationshipComments'

    id = sa.Column(sa.Integer, primary_key=True)
    relationshipid = sa.Column(sa.Integer, sa.ForeignKey('Relationship.id'))
    dateadded = sa.Column(sa.Date)
    commentdata = sa.Column(sa.LargeBinary)

    relationship = orm.relationship('Relationship', back_populates='comments')



