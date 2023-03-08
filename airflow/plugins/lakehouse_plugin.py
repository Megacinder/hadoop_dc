import json

from airflow.plugins_manager import AirflowPlugin
from airflow.security import permissions
from airflow.www.views import AirflowModelView
from flask import Blueprint, redirect
from flask_appbuilder import action
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, SelectField, validators, TextAreaField, TextField
from wtforms.fields.html5 import DateField

from plugins.models.databasesource import DatabaseSource, Load, LoadType

# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "lakehouse", __name__,
    template_folder='templates',  # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/static/lakehouse')


class JSONField(TextAreaField):
    def _value(self):
        return json.dumps(self.data) if self.data else ''

    def process_formdata(self, valuelist):
        data = valuelist[0]
        if data:
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                raise ValueError('This field contains invalid JSON')
        else:
            self.data = None

    def process_data(self, value):
        self.data = value

    def pre_validate(self, form):
        if self.data:
            try:
                json.dumps(self.data)
            except TypeError:
                raise ValueError('This field contains invalid JSON')


class DatabaseSourceEditForm(DynamicForm):
    """Form for editing DatabaseSource"""

    table_name = StringField("Table name")
    schema = StringField("Schema")
    load = SelectField("Load", choices=Load.choices(), coerce=Load.coerce)
    load_type = SelectField("Load Type", choices=LoadType.choices(), coerce=LoadType.coerce)
    last_load_type = SelectField("Last Load Type", choices=LoadType.choices(), coerce=LoadType.coerce)
    next_load_type = SelectField("Next Load Type", choices=LoadType.choices(), coerce=LoadType.coerce)
    spark_submit = JSONField("Spark-submit")
    target_options = JSONField("Target options")
    jdbc_options = JSONField("jdbc options")
    sql_script = TextField("SQL script")
    incremental_load_date = DateField("Incremental Date", format='%Y-%m-%d', validators=(validators.Optional(),))


class DatabaseSourceModelView(AirflowModelView):
    route_base = "/databasesource"

    datamodel = AirflowModelView.CustomSQLAInterface(DatabaseSource)

    class_permission_name = permissions.RESOURCE_CONNECTION
    method_permission_name = {
        'add': 'create',
        'list': 'read',
        'edit': 'edit',
        'delete': 'delete',
        'action_muldelete': 'delete',
    }

    base_permissions = [
        permissions.ACTION_CAN_CREATE,
        permissions.ACTION_CAN_READ,
        permissions.ACTION_CAN_EDIT,
        permissions.ACTION_CAN_DELETE,
        permissions.ACTION_CAN_ACCESS_MENU,
    ]

    list_columns = ["table_name",
                    "schema",
                    "load",
                    "last_load_date",
                    "load_type",
                    "last_load_type",
                    "next_load_type",
                    "spark_submit",
                    "target_options",
                    "jdbc_options",
                    "sql_script",
                    "incremental_load_date"]
    add_columns = ["table_name",
                   "schema",
                   "load",
                   "load_type",
                   "last_load_type",
                   "next_load_type",
                   "spark_submit",
                   "target_options",
                   "jdbc_options",
                   "sql_script",
                   "incremental_load_date"]
    edit_columns = ["table_name",
                    "schema",
                    "load",
                    "load_type",
                    "last_load_type",
                    "next_load_type",
                    "spark_submit",
                    "target_options",
                    "jdbc_options",
                    "sql_script",
                    "incremental_load_date"]
    edit_form = add_form = DatabaseSourceEditForm

    base_order = ('table_name', 'asc')
    search_exclude_columns = ['spark_submit', 'target_options', 'jdbc_options']

    @action("set_load_yes", "Set Load to 'Y'")
    def action_set_load_yes(self, items):
        if isinstance(items, list):
            for item in items:
                item.load = Load.Y.name
                self.datamodel.edit(item)
                self.update_redirect()
        else:
            items.load = Load.Y.name
            self.datamodel.edit(items)
        return redirect(self.get_redirect())

    @action("set_load_no", "Set Load to 'N'")
    def action_set_load_no(self, items):
        if isinstance(items, list):
            for item in items:
                item.load = Load.N.name
                self.datamodel.edit(item)
                self.update_redirect()
        else:
            items.load = Load.N.name
            self.datamodel.edit(items)
        return redirect(self.get_redirect())

    @action("next_load_full", "Set Next Load to 'FULL'")
    def action_next_load_full(self, items):
        if isinstance(items, list):
            for item in items:
                item.next_load_type = LoadType.FULL.name
                self.datamodel.edit(item)
                self.update_redirect()
        else:
            items.next_load_type = LoadType.FULL.name
            self.datamodel.edit(items)
        return redirect(self.get_redirect())

    @action("next_load_incremental", "Set Next Load to 'INCREMENTAL'")
    def action_next_load_incremental(self, items):
        if isinstance(items, list):
            for item in items:
                item.next_load_type = LoadType.INCREMENTAL.name
                self.datamodel.edit(item)
                self.update_redirect()
        else:
            items.next_load_type = LoadType.INCREMENTAL.name
            self.datamodel.edit(items)
        return redirect(self.get_redirect())


appbuilder_view = DatabaseSourceModelView()
appbuilder_package = {"name": "Database Source",
                      "category": "Lakehouse",
                      "view": appbuilder_view}


class LakeHousePlugin(AirflowPlugin):
    name = "LakehousePlugin"
    hooks = []
    macros = []
    flask_blueprints = [bp, ]
    appbuilder_views = [appbuilder_package, ]
    appbuilder_menu_items = []
    global_operator_extra_links = []
    operator_extra_links = []
