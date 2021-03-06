from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_create="",
                 sql_insert="",
                 mode="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.table=table
        self.sql_create=sql_create
        self.sql_insert=sql_insert
        self.mode=mode

    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f"Create {self.table} dim table")
        redshift_hook.run(f"{self.sql_create}")
        
        columns = ""
        if self.table in ("vaccines_dim","source_dim"):
            columns = "(name)"
            
        
        if self.mode == "delete-load":
            self.log.info(f"DELETE {self.table} dim tables")
            redshift_hook.run(f"DELETE FROM {self.table};")
        
        self.log.info(f"INSERT DATA INTO {self.table}")
        redshift_hook.run(f"INSERT INTO {self.table} {columns} {self.sql_insert}")