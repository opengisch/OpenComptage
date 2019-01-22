<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.3-Madeira" maxScale="0" readOnly="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="dd-MM-yyyy" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" name="CheckedState" type="QString"/>
            <Option value="" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" name="CheckedState" type="QString"/>
            <Option value="" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="model_858d7992_6320_4172_8c77_79897a7ed764" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="automate_cfd1f05d_776c_42cd_a574_429c7d001278" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="type_capteur_03c54e75_9682_41d8_ac3e_9419087eb24c" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="classification_20773e1b_c83e_4287_b12b_9685e886ae09" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="installation_4ea85e41_1de8_4149_a710_f0b44d137284" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="start_service_date" index="1" name="Début service"/>
    <alias field="end_service_date" index="2" name="Fin service"/>
    <alias field="start_put_date" index="3" name="Début pose"/>
    <alias field="end_put_date" index="4" name="Fin pose"/>
    <alias field="start_process_date" index="5" name="Début traitement"/>
    <alias field="end_process_date" index="6" name="Fin traitement"/>
    <alias field="valid" index="7" name="Valide"/>
    <alias field="dysfunction" index="8" name="Dysfonctionnement"/>
    <alias field="remarks" index="9" name="Remarques"/>
    <alias field="id_model" index="10" name="Model"/>
    <alias field="id_device" index="11" name="Automate"/>
    <alias field="id_sensor_type" index="12" name="Type capteur"/>
    <alias field="id_class" index="13" name="Classification"/>
    <alias field="id_installation" index="14" name="Installation"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="start_service_date" applyOnUpdate="0" expression="''"/>
    <default field="end_service_date" applyOnUpdate="0" expression=""/>
    <default field="start_put_date" applyOnUpdate="0" expression=""/>
    <default field="end_put_date" applyOnUpdate="0" expression=""/>
    <default field="start_process_date" applyOnUpdate="0" expression=""/>
    <default field="end_process_date" applyOnUpdate="0" expression=""/>
    <default field="valid" applyOnUpdate="0" expression=""/>
    <default field="dysfunction" applyOnUpdate="0" expression=""/>
    <default field="remarks" applyOnUpdate="0" expression=""/>
    <default field="id_model" applyOnUpdate="0" expression=""/>
    <default field="id_device" applyOnUpdate="0" expression=""/>
    <default field="id_sensor_type" applyOnUpdate="0" expression=""/>
    <default field="id_class" applyOnUpdate="0" expression=""/>
    <default field="id_installation" applyOnUpdate="0" expression="@selected_installation"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="start_service_date" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="end_service_date" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="start_put_date" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="end_put_date" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="start_process_date" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="end_process_date" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="valid" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="dysfunction" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="remarks" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_model" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="id_device" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_sensor_type" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_class" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_installation" constraints="1" exp_strength="0" notnull_strength="2"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="start_service_date" exp=""/>
    <constraint desc="" field="end_service_date" exp=""/>
    <constraint desc="" field="start_put_date" exp=""/>
    <constraint desc="" field="end_put_date" exp=""/>
    <constraint desc="" field="start_process_date" exp=""/>
    <constraint desc="" field="end_process_date" exp=""/>
    <constraint desc="" field="valid" exp=""/>
    <constraint desc="" field="dysfunction" exp=""/>
    <constraint desc="" field="remarks" exp=""/>
    <constraint desc="" field="id_model" exp=""/>
    <constraint desc="" field="id_device" exp=""/>
    <constraint desc="" field="id_sensor_type" exp=""/>
    <constraint desc="" field="id_class" exp=""/>
    <constraint desc="" field="id_installation" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting capture="0" notificationMessage="" name="Exporter la configuration" isEnabledOnlyWhenEditable="0" shortTitle="" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" id="{ff4abd1b-0700-49aa-968d-e8314a7e7518}" type="1">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" name="Importation" isEnabledOnlyWhenEditable="0" shortTitle="" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])" id="{011debe3-1100-4193-afda-6787a40c4bdd}" type="1">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" name="Creer un rapport" isEnabledOnlyWhenEditable="0" shortTitle="" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" id="{c930464a-cdd6-40ff-989f-d87ad4273422}" type="1">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" name="Creer un plan" isEnabledOnlyWhenEditable="0" shortTitle="" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" id="{64fe4013-1ed6-425b-88de-eb6f2684437a}" type="1">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" name="Générer les graphiques" isEnabledOnlyWhenEditable="0" shortTitle="" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" id="{7b092ff8-4fc1-496c-a9f1-83b3eaea8d0d}" type="1">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="start_service_date" type="field"/>
      <column width="-1" hidden="0" name="end_service_date" type="field"/>
      <column width="-1" hidden="0" name="start_put_date" type="field"/>
      <column width="-1" hidden="0" name="end_put_date" type="field"/>
      <column width="-1" hidden="0" name="start_process_date" type="field"/>
      <column width="-1" hidden="0" name="end_process_date" type="field"/>
      <column width="-1" hidden="0" name="valid" type="field"/>
      <column width="-1" hidden="0" name="dysfunction" type="field"/>
      <column width="-1" hidden="0" name="remarks" type="field"/>
      <column width="-1" hidden="0" name="id_model" type="field"/>
      <column width="-1" hidden="0" name="id_device" type="field"/>
      <column width="-1" hidden="0" name="id_sensor_type" type="field"/>
      <column width="-1" hidden="0" name="id_class" type="field"/>
      <column width="-1" hidden="0" name="id_installation" type="field"/>
      <column width="-1" hidden="0" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit>on_form_open</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import QDate
from functools import partial


def on_form_open(dialog, layer, feature):
	dialog.widgetValueChanged.connect(partial(on_dialog_changed, dialog))
	
def on_dialog_changed(dialog, attribute, value, attributeChanged):
	print(dialog)
	if attributeChanged:
		if attribute == 'start_service_date':
			dialog.changeAttribute('end_service_date', value.addDays(14), '')
			dialog.changeAttribute('start_put_date', value, '')
			dialog.changeAttribute('end_put_date', value.addDays(14), '')
			dialog.changeAttribute('start_process_date', value, '')
			dialog.changeAttribute('end_process_date', value.addDays(14), '')
		if attribute == 'start_put_date':
			dialog.changeAttribute('end_put_date', value.addDays(14), '')
		if attribute == 'start_process_date':
			dialog.changeAttribute('end_process_date', value.addDays(14), '')]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="dysfunction"/>
    <field editable="1" name="end_process_date"/>
    <field editable="1" name="end_put_date"/>
    <field editable="1" name="end_service_date"/>
    <field editable="1" name="id"/>
    <field editable="1" name="id_class"/>
    <field editable="1" name="id_device"/>
    <field editable="0" name="id_installation"/>
    <field editable="1" name="id_model"/>
    <field editable="1" name="id_sensor_type"/>
    <field editable="1" name="remarks"/>
    <field editable="1" name="start_process_date"/>
    <field editable="1" name="start_put_date"/>
    <field editable="1" name="start_service_date"/>
    <field editable="1" name="valid"/>
  </editable>
  <labelOnTop>
    <field name="dysfunction" labelOnTop="0"/>
    <field name="end_process_date" labelOnTop="0"/>
    <field name="end_put_date" labelOnTop="0"/>
    <field name="end_service_date" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="id_class" labelOnTop="0"/>
    <field name="id_device" labelOnTop="0"/>
    <field name="id_installation" labelOnTop="0"/>
    <field name="id_model" labelOnTop="0"/>
    <field name="id_sensor_type" labelOnTop="0"/>
    <field name="remarks" labelOnTop="0"/>
    <field name="start_process_date" labelOnTop="0"/>
    <field name="start_put_date" labelOnTop="0"/>
    <field name="start_service_date" labelOnTop="0"/>
    <field name="valid" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
