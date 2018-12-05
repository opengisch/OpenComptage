<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.2.3-Bonn" readOnly="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0" maxScale="0">
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
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="dd-MM-yyyy"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value=""/>
            <Option type="QString" name="UncheckedState" value=""/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value=""/>
            <Option type="QString" name="UncheckedState" value=""/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="true"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowMulti" value="false"/>
            <Option type="bool" name="AllowNull" value="false"/>
            <Option type="QString" name="FilterExpression" value=""/>
            <Option type="QString" name="Key" value="id"/>
            <Option type="QString" name="Layer" value="model_cfdf7370_1fa1_4013_81c8_510c4bfee920"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowMulti" value="false"/>
            <Option type="bool" name="AllowNull" value="false"/>
            <Option type="QString" name="FilterExpression" value=""/>
            <Option type="QString" name="Key" value="id"/>
            <Option type="QString" name="Layer" value="automate_883001d3_b5e2_40e7_8803_d5ffc6a5bfd1"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowMulti" value="false"/>
            <Option type="bool" name="AllowNull" value="false"/>
            <Option type="QString" name="FilterExpression" value=""/>
            <Option type="QString" name="Key" value="id"/>
            <Option type="QString" name="Layer" value="type_capteur_31ea7157_02dc_4c41_a7a9_faaf866a4d72"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowMulti" value="false"/>
            <Option type="bool" name="AllowNull" value="false"/>
            <Option type="QString" name="FilterExpression" value=""/>
            <Option type="QString" name="Key" value="id"/>
            <Option type="QString" name="Layer" value="classification_e202f34e_f5f8_432c_9fa3_c7a97f138b9e"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowMulti" value="false"/>
            <Option type="bool" name="AllowNull" value="false"/>
            <Option type="QString" name="FilterExpression" value=""/>
            <Option type="QString" name="Key" value="id"/>
            <Option type="QString" name="Layer" value="installation_9fb595b0_2d45_4184_816b_d289ceb978ab"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
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
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="start_service_date" applyOnUpdate="0"/>
    <default expression="" field="end_service_date" applyOnUpdate="0"/>
    <default expression="" field="start_put_date" applyOnUpdate="0"/>
    <default expression="" field="end_put_date" applyOnUpdate="0"/>
    <default expression="" field="start_process_date" applyOnUpdate="0"/>
    <default expression="" field="end_process_date" applyOnUpdate="0"/>
    <default expression="" field="valid" applyOnUpdate="0"/>
    <default expression="" field="dysfunction" applyOnUpdate="0"/>
    <default expression="" field="remarks" applyOnUpdate="0"/>
    <default expression="" field="id_model" applyOnUpdate="0"/>
    <default expression="" field="id_device" applyOnUpdate="0"/>
    <default expression="" field="id_sensor_type" applyOnUpdate="0"/>
    <default expression="" field="id_class" applyOnUpdate="0"/>
    <default expression="@selected_installation" field="id_installation" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" exp_strength="0" unique_strength="1" constraints="3" notnull_strength="1"/>
    <constraint field="start_service_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="end_service_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="start_put_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="end_put_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="start_process_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="end_process_date" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="valid" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="dysfunction" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="remarks" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_model" exp_strength="0" unique_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_device" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_sensor_type" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_class" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_installation" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="start_service_date" desc=""/>
    <constraint exp="" field="end_service_date" desc=""/>
    <constraint exp="" field="start_put_date" desc=""/>
    <constraint exp="" field="end_put_date" desc=""/>
    <constraint exp="" field="start_process_date" desc=""/>
    <constraint exp="" field="end_process_date" desc=""/>
    <constraint exp="" field="valid" desc=""/>
    <constraint exp="" field="dysfunction" desc=""/>
    <constraint exp="" field="remarks" desc=""/>
    <constraint exp="" field="id_model" desc=""/>
    <constraint exp="" field="id_device" desc=""/>
    <constraint exp="" field="id_sensor_type" desc=""/>
    <constraint exp="" field="id_class" desc=""/>
    <constraint exp="" field="id_installation" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting icon="" id="{cb2213e7-9e08-4030-8919-b04df157a611}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" notificationMessage="" shortTitle="" type="1" name="Export configuration" capture="0" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" id="{f9f8e89a-ea0c-4da8-bf4a-e528901309fd}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_data_action([% $id %])" notificationMessage="" shortTitle="" type="1" name="Import data" capture="0" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" id="{c3d66c77-d09f-487f-b0d5-312884bbb8c6}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" notificationMessage="" shortTitle="" type="1" name="Create report" capture="0" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" id="{9d7724b4-baa4-49b5-aef8-9df31680a673}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" notificationMessage="" shortTitle="" type="1" name="Export plan" capture="0" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" id="{f716b958-0464-422d-b21e-0b80a2da3a3a}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" notificationMessage="" shortTitle="" type="1" name="Generate chart" capture="0" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="id" hidden="0" width="-1"/>
      <column type="field" name="start_service_date" hidden="0" width="-1"/>
      <column type="field" name="end_service_date" hidden="0" width="-1"/>
      <column type="field" name="start_put_date" hidden="0" width="-1"/>
      <column type="field" name="end_put_date" hidden="0" width="-1"/>
      <column type="field" name="start_process_date" hidden="0" width="-1"/>
      <column type="field" name="end_process_date" hidden="0" width="-1"/>
      <column type="field" name="valid" hidden="0" width="-1"/>
      <column type="field" name="dysfunction" hidden="0" width="-1"/>
      <column type="field" name="remarks" hidden="0" width="-1"/>
      <column type="field" name="id_model" hidden="0" width="-1"/>
      <column type="field" name="id_device" hidden="0" width="-1"/>
      <column type="field" name="id_sensor_type" hidden="0" width="-1"/>
      <column type="field" name="id_class" hidden="0" width="-1"/>
      <column type="field" name="id_installation" hidden="0" width="-1"/>
      <column type="actions" hidden="0" width="-1"/>
    </columns>
  </attributetableconfig>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
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
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
