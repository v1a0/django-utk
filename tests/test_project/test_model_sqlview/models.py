from django_utk.db.models import DBViewModel


class SimpleSQLView(DBViewModel):

    class Meta:
        managed = False
        db_table = "simple_sql_view"
