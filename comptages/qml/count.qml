<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0" version="3.2.3-Bonn" readOnly="0">
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
            <Option type="QString" name="Layer" value="model_b53128ed_8b7a_47df_a852_04d1e2ecf896"/>
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
            <Option type="QString" name="Layer" value="automate_c362d4f9_adcd_47ae_9d86_90c33ed4e3fd"/>
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
            <Option type="QString" name="Layer" value="type_capteur_cdc741e9_cd3d_41b4_b48f_266260c0b816"/>
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
            <Option type="QString" name="Layer" value="classification_d1914a6f_de56_4f55_b327_be84d5debc1b"/>
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
            <Option type="QString" name="Layer" value="installation_fdd20315_81d0_49f3_90f4_0b896d1260e1"/>
            <Option type="int" name="NofColumns" value="1"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="UseCompleter" value="false"/>
            <Option type="QString" name="Value" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="id"/>
    <alias index="1" name="Début service" field="start_service_date"/>
    <alias index="2" name="Fin service" field="end_service_date"/>
    <alias index="3" name="Début pose" field="start_put_date"/>
    <alias index="4" name="Fin pose" field="end_put_date"/>
    <alias index="5" name="Début traitement" field="start_process_date"/>
    <alias index="6" name="Fin traitement" field="end_process_date"/>
    <alias index="7" name="Valide" field="valid"/>
    <alias index="8" name="Dysfonctionnement" field="dysfunction"/>
    <alias index="9" name="Remarques" field="remarks"/>
    <alias index="10" name="Model" field="id_model"/>
    <alias index="11" name="Automate" field="id_device"/>
    <alias index="12" name="Type capteur" field="id_sensor_type"/>
    <alias index="13" name="Classification" field="id_class"/>
    <alias index="14" name="Installation" field="id_installation"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="start_service_date" expression=""/>
    <default applyOnUpdate="0" field="end_service_date" expression=""/>
    <default applyOnUpdate="0" field="start_put_date" expression=""/>
    <default applyOnUpdate="0" field="end_put_date" expression=""/>
    <default applyOnUpdate="0" field="start_process_date" expression=""/>
    <default applyOnUpdate="0" field="end_process_date" expression=""/>
    <default applyOnUpdate="0" field="valid" expression=""/>
    <default applyOnUpdate="0" field="dysfunction" expression=""/>
    <default applyOnUpdate="0" field="remarks" expression=""/>
    <default applyOnUpdate="0" field="id_model" expression=""/>
    <default applyOnUpdate="0" field="id_device" expression=""/>
    <default applyOnUpdate="0" field="id_sensor_type" expression=""/>
    <default applyOnUpdate="0" field="id_class" expression=""/>
    <default applyOnUpdate="0" field="id_installation" expression="@selected_installation"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" constraints="3" exp_strength="0" field="id"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="start_service_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="end_service_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="start_put_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="end_put_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="start_process_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="end_process_date"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="valid"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="dysfunction"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="remarks"/>
    <constraint notnull_strength="1" unique_strength="0" constraints="1" exp_strength="0" field="id_model"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="id_device"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="id_sensor_type"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="id_class"/>
    <constraint notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0" field="id_installation"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="start_service_date" exp="" desc=""/>
    <constraint field="end_service_date" exp="" desc=""/>
    <constraint field="start_put_date" exp="" desc=""/>
    <constraint field="end_put_date" exp="" desc=""/>
    <constraint field="start_process_date" exp="" desc=""/>
    <constraint field="end_process_date" exp="" desc=""/>
    <constraint field="valid" exp="" desc=""/>
    <constraint field="dysfunction" exp="" desc=""/>
    <constraint field="remarks" exp="" desc=""/>
    <constraint field="id_model" exp="" desc=""/>
    <constraint field="id_device" exp="" desc=""/>
    <constraint field="id_sensor_type" exp="" desc=""/>
    <constraint field="id_class" exp="" desc=""/>
    <constraint field="id_installation" exp="" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting type="1" capture="0" isEnabledOnlyWhenEditable="0" name="Export configuration" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" notificationMessage="" shortTitle="" id="{7abdab30-c552-4815-a0f1-8eeb7b974e9e}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" capture="0" isEnabledOnlyWhenEditable="0" name="Import data" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_data_action([% $id %])" notificationMessage="" shortTitle="" id="{19757617-0afd-4820-ac60-51edb63389f3}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" capture="0" isEnabledOnlyWhenEditable="0" name="Create report" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" notificationMessage="" shortTitle="" id="{5ae5ee58-201f-4a75-8267-ef4d960d9a45}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" capture="0" isEnabledOnlyWhenEditable="0" name="Export plan" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" notificationMessage="" shortTitle="" id="{10aa19b5-13d2-4f57-af88-bb2177c43d37}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" capture="0" isEnabledOnlyWhenEditable="0" name="Generate chart" icon="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" notificationMessage="" shortTitle="" id="{09366f33-2f99-4d99-a1de-0009d7d4f14a}">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="field" hidden="0" name="id" width="-1"/>
      <column type="field" hidden="0" name="start_service_date" width="-1"/>
      <column type="field" hidden="0" name="end_service_date" width="-1"/>
      <column type="field" hidden="0" name="start_put_date" width="-1"/>
      <column type="field" hidden="0" name="end_put_date" width="-1"/>
      <column type="field" hidden="0" name="start_process_date" width="-1"/>
      <column type="field" hidden="0" name="end_process_date" width="-1"/>
      <column type="field" hidden="0" name="valid" width="-1"/>
      <column type="field" hidden="0" name="dysfunction" width="-1"/>
      <column type="field" hidden="0" name="remarks" width="-1"/>
      <column type="field" hidden="0" name="id_model" width="-1"/>
      <column type="field" hidden="0" name="id_device" width="-1"/>
      <column type="field" hidden="0" name="id_sensor_type" width="-1"/>
      <column type="field" hidden="0" name="id_class" width="-1"/>
      <column type="field" hidden="0" name="id_installation" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
    <field name="dysfunction" editable="1"/>
    <field name="end_process_date" editable="1"/>
    <field name="end_put_date" editable="1"/>
    <field name="end_service_date" editable="1"/>
    <field name="id" editable="1"/>
    <field name="id_class" editable="1"/>
    <field name="id_device" editable="1"/>
    <field name="id_installation" editable="0"/>
    <field name="id_model" editable="1"/>
    <field name="id_sensor_type" editable="1"/>
    <field name="remarks" editable="1"/>
    <field name="start_process_date" editable="1"/>
    <field name="start_put_date" editable="1"/>
    <field name="start_service_date" editable="1"/>
    <field name="valid" editable="1"/>
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
