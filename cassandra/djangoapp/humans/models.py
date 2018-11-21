import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class Humans(DjangoCassandraModel):
    sr_no = columns.Integer(primary_key=True)
    refund = columns.Text(required=False)
    m_status = columns.Text(required=False)
    income = columns.Text(required=False)
    cheat = columns.Text(required=False)