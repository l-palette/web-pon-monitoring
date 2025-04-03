from database import db
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=True)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

class Topic(db.Model):
    __tablename__ = 'topic'
    topic_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)

class Reply(db.Model):
    __tablename__ = 'reply'
    reply_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

class Host(db.Model):
    __tablename__ = 'hosts'
    hostid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zbxhostid = db.Column(db.Integer, unique=True)
    zbxhost = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text)

    ip_addresses = db.relationship('IPAddress', backref='host', lazy=True)
    pon_monitorings = db.relationship('PonMonitoring', backref='host', lazy=True)

class Group(db.Model):
    __tablename__ = 'groups'
    groupid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zbxgroupid = db.Column(db.Integer, unique=True)
    zbxgroup = db.Column(db.Text, nullable=False)

class HostGroup(db.Model):
    __tablename__ = 'hostgroup'
    hostgroupid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostid = db.Column(db.Integer, db.ForeignKey('hosts.hostid'), nullable=False)
    groupid = db.Column(db.Integer, db.ForeignKey('groups.groupid'), nullable=False)

    __table_args__ = (UniqueConstraint('hostid', 'groupid', name='uix_host_group'),)

class IPAddress(db.Model):
    __tablename__ = 'ipaddresses'
    ipid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostid = db.Column(db.Integer, db.ForeignKey('hosts.hostid'), nullable=False)
    ip = db.Column(db.Text, nullable=False)

class PonMonitoring(db.Model):
    __tablename__ = 'ponmonitoring'
    ponid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostid = db.Column(db.Integer, db.ForeignKey('hosts.hostid'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    serialnumber = db.Column(db.Text)
    interfaceid = db.Column(db.Text)
    interfacename = db.Column(db.Text)

    __table_args__ = (UniqueConstraint('hostid', name='uix_host_pon'),)
