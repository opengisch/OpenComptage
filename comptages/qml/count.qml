<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.2.3-Bonn" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
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
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" value="true" type="bool"/>
            <Option name="calendar_popup" value="true" type="bool"/>
            <Option name="display_format" value="dd-MM-yyyy" type="QString"/>
            <Option name="field_format" value="yyyy-MM-dd" type="QString"/>
            <Option name="field_iso_format" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="" type="QString"/>
            <Option name="UncheckedState" value="" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="" type="QString"/>
            <Option name="UncheckedState" value="" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="true" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" value="false" type="bool"/>
            <Option name="AllowNull" value="false" type="bool"/>
            <Option name="FilterExpression" value="" type="QString"/>
            <Option name="Key" value="id" type="QString"/>
            <Option name="Layer" value="model_0a4efa69_e99e_42cb_bcd4_bc25e0beb994" type="QString"/>
            <Option name="NofColumns" value="1" type="int"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="UseCompleter" value="false" type="bool"/>
            <Option name="Value" value="name" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" value="false" type="bool"/>
            <Option name="AllowNull" value="false" type="bool"/>
            <Option name="FilterExpression" value="" type="QString"/>
            <Option name="Key" value="id" type="QString"/>
            <Option name="Layer" value="automate_f8543fba_67fa_4a81_8c64_acd96b6d17d5" type="QString"/>
            <Option name="NofColumns" value="1" type="int"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="UseCompleter" value="false" type="bool"/>
            <Option name="Value" value="name" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" value="false" type="bool"/>
            <Option name="AllowNull" value="false" type="bool"/>
            <Option name="FilterExpression" value="" type="QString"/>
            <Option name="Key" value="id" type="QString"/>
            <Option name="Layer" value="type_capteur_034956b2_8bed_4e97_b78d_7217c6f22308" type="QString"/>
            <Option name="NofColumns" value="1" type="int"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="UseCompleter" value="false" type="bool"/>
            <Option name="Value" value="name" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" value="false" type="bool"/>
            <Option name="AllowNull" value="false" type="bool"/>
            <Option name="FilterExpression" value="" type="QString"/>
            <Option name="Key" value="id" type="QString"/>
            <Option name="Layer" value="classification_fab24724_be97_456b_85dd_14ca851204f1" type="QString"/>
            <Option name="NofColumns" value="1" type="int"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="UseCompleter" value="false" type="bool"/>
            <Option name="Value" value="name" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="RelationReference">
        <config>
          <Option type="Map">
            <Option name="AllowAddFeatures" value="false" type="bool"/>
            <Option name="AllowNULL" value="false" type="bool"/>
            <Option name="MapIdentification" value="false" type="bool"/>
            <Option name="OrderByValue" value="false" type="bool"/>
            <Option name="ReadOnly" value="false" type="bool"/>
            <Option name="Relation" value="rel_installation_count" type="QString"/>
            <Option name="ShowForm" value="false" type="bool"/>
            <Option name="ShowOpenFormButton" value="true" type="bool"/>
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
    <default expression="" field="id_installation" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="1" field="id" constraints="3" notnull_strength="1"/>
    <constraint exp_strength="0" unique_strength="0" field="start_service_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="end_service_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="start_put_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="end_put_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="start_process_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="end_process_date" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="valid" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="dysfunction" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="remarks" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="id_model" constraints="1" notnull_strength="1"/>
    <constraint exp_strength="0" unique_strength="0" field="id_device" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="id_sensor_type" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="id_class" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" field="id_installation" constraints="0" notnull_strength="0"/>
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
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
    <actionsetting name="Export configuration" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].export_configuration([% $id %])" icon="" type="1" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" id="{378e8101-0719-49f1-9978-2b03de64d75f}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Import data" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].import_data([% $id %])" icon="" type="1" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" id="{9c42788b-c86c-4228-9893-cfca416f02b2}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Create report" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].create_report([% $id %])" icon="" type="1" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" id="{9df8af8e-cf75-4176-baac-a354663025ce}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Export plan" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].export_plan([% $id %])" icon="" type="1" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" id="{0257f030-089b-428e-95f6-f09c1daeecbd}">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="id" type="field" width="-1" hidden="0"/>
      <column name="start_service_date" type="field" width="-1" hidden="0"/>
      <column name="end_service_date" type="field" width="-1" hidden="0"/>
      <column name="start_put_date" type="field" width="-1" hidden="0"/>
      <column name="end_put_date" type="field" width="-1" hidden="0"/>
      <column name="start_process_date" type="field" width="-1" hidden="0"/>
      <column name="end_process_date" type="field" width="-1" hidden="0"/>
      <column name="valid" type="field" width="-1" hidden="0"/>
      <column name="dysfunction" type="field" width="-1" hidden="0"/>
      <column name="remarks" type="field" width="-1" hidden="0"/>
      <column name="id_model" type="field" width="-1" hidden="0"/>
      <column name="id_device" type="field" width="-1" hidden="0"/>
      <column name="id_sensor_type" type="field" width="-1" hidden="0"/>
      <column name="id_class" type="field" width="-1" hidden="0"/>
      <column name="id_installation" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <field name="id_installation" editable="1"/>
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
