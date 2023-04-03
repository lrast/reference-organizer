# ORM data model
import sqlalchemy as sa
import sqlalchemy.orm as orm

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Edges
class PageTopicAssociation(db.Model):
    __tablename__ = 'PageTopic'
    id = sa.Column(sa.Integer, primary_key=True)
    pageid = sa.Column(sa.Integer, sa.ForeignKey('Page.id'))
    topicid = sa.Column(sa.Integer, sa.ForeignKey('Topic.id'))


class TopicTopicAssociation(db.Model):
    __tablename__ = 'TopicTopicRelationship'
    id = sa.Column(sa.Integer, primary_key=True)
    relationshipid = sa.Column(sa.Integer, sa.ForeignKey('Relationship.id'))
    lefttopicid = sa.Column(sa.Integer, sa.ForeignKey('Topic.id'))
    righttopicid = sa.Column(sa.Integer, sa.ForeignKey('Topic.id'))

    righttopic = orm.relationship('Topic', foreign_keys=[righttopicid])
    lefttopic = orm.relationship('Topic', foreign_keys=[lefttopicid])


class PagePageAssociation(db.Model):
    __tablename__ = 'PagePageRelationship'
    id = sa.Column(sa.Integer, primary_key=True)
    relationshipid = sa.Column(sa.Integer, sa.ForeignKey('Relationship.id'))
    leftpageid = sa.Column(sa.Integer, sa.ForeignKey('Page.id'))
    rightpageid = sa.Column(sa.Integer, sa.ForeignKey('Page.id'))

    rightpage = orm.relationship('Page', foreign_keys=[rightpageid])
    leftpage = orm.relationship('Page', foreign_keys=[leftpageid])



# Nodes
class Page(db.Model):
    __tablename__ = 'Page'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column( sa.String, unique=True, nullable=False)
    name = sa.Column( sa.String )
    dateadded = sa.Column( sa.Date )

    topics = orm.relationship('Topic', secondary=PageTopicAssociation.__table__, back_populates='pages')
    comments = orm.relationship('PageComments', back_populates='page')

    rightPages = orm.relationship('Page', secondary=PagePageAssociation.__table__,
        primaryjoin=(PagePageAssociation.leftpageid == id),
        secondaryjoin=(PagePageAssociation.rightpageid == id),
        backref = 'leftPages'
        )

class Topic(db.Model):
    __tablename__ = 'Topic'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    pages = orm.relationship('Page', secondary=PageTopicAssociation.__table__, back_populates='topics')
    comments = orm.relationship('TopicComments', back_populates='topic')

    rightTopics = orm.relationship('Topic', secondary=TopicTopicAssociation.__table__,
        primaryjoin=(TopicTopicAssociation.lefttopicid == id),
        secondaryjoin=(TopicTopicAssociation.righttopicid == id),
        backref = 'leftTopics'
        )

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

