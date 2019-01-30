<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" version="3.4.3-Madeira" minScale="1e+08" maxScale="0" readOnly="0" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>id</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
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
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="dd-MM-yyyy" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" type="QString" name="CheckedState"/>
            <Option value="" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" type="QString" name="CheckedState"/>
            <Option value="" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="model_cc014b15_ab01_4104_a167_96664b89cf49" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="automate_ea92567d_99be_44cc_8d67_291d55fff545" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="type_capteur_9adb705c_d60c_46be_994d_9db8d89cad83" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="classification_fc7736a3_e3c7_42db_9a61_0a5c87c5f0e1" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="installation_26366269_638e_46b3_9a47_fc47e7fc82a2" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Periode speciale">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="Début service" index="1" field="start_service_date"/>
    <alias name="Fin service" index="2" field="end_service_date"/>
    <alias name="Début pose" index="3" field="start_put_date"/>
    <alias name="Fin pose" index="4" field="end_put_date"/>
    <alias name="Début traitement" index="5" field="start_process_date"/>
    <alias name="Fin traitement" index="6" field="end_process_date"/>
    <alias name="Valide" index="7" field="valid"/>
    <alias name="Dysfonctionnement" index="8" field="dysfunction"/>
    <alias name="Remarques" index="9" field="remarks"/>
    <alias name="Model" index="10" field="id_model"/>
    <alias name="Automate" index="11" field="id_device"/>
    <alias name="Type capteur" index="12" field="id_sensor_type"/>
    <alias name="Classification" index="13" field="id_class"/>
    <alias name="Installation" index="14" field="id_installation"/>
    <alias name="" index="15" field="Periode speciale"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="id"/>
    <default expression="''" applyOnUpdate="0" field="start_service_date"/>
    <default expression="" applyOnUpdate="0" field="end_service_date"/>
    <default expression="" applyOnUpdate="0" field="start_put_date"/>
    <default expression="" applyOnUpdate="0" field="end_put_date"/>
    <default expression="" applyOnUpdate="0" field="start_process_date"/>
    <default expression="" applyOnUpdate="0" field="end_process_date"/>
    <default expression="" applyOnUpdate="0" field="valid"/>
    <default expression="" applyOnUpdate="0" field="dysfunction"/>
    <default expression="" applyOnUpdate="0" field="remarks"/>
    <default expression="" applyOnUpdate="0" field="id_model"/>
    <default expression="" applyOnUpdate="0" field="id_device"/>
    <default expression="" applyOnUpdate="0" field="id_sensor_type"/>
    <default expression="" applyOnUpdate="0" field="id_class"/>
    <default expression="@selected_installation" applyOnUpdate="0" field="id_installation"/>
    <default expression="" applyOnUpdate="0" field="Periode speciale"/>
  </defaults>
  <constraints>
    <constraint constraints="3" notnull_strength="1" exp_strength="0" unique_strength="1" field="id"/>
    <constraint constraints="1" notnull_strength="2" exp_strength="0" unique_strength="0" field="start_service_date"/>
    <constraint constraints="1" notnull_strength="2" exp_strength="0" unique_strength="0" field="end_service_date"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="start_put_date"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="end_put_date"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="start_process_date"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="end_process_date"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="valid"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="dysfunction"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="remarks"/>
    <constraint constraints="1" notnull_strength="1" exp_strength="0" unique_strength="0" field="id_model"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="id_device"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="id_sensor_type"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="id_class"/>
    <constraint constraints="1" notnull_strength="2" exp_strength="0" unique_strength="0" field="id_installation"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0" field="Periode speciale"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="start_service_date"/>
    <constraint desc="" exp="" field="end_service_date"/>
    <constraint desc="" exp="" field="start_put_date"/>
    <constraint desc="" exp="" field="end_put_date"/>
    <constraint desc="" exp="" field="start_process_date"/>
    <constraint desc="" exp="" field="end_process_date"/>
    <constraint desc="" exp="" field="valid"/>
    <constraint desc="" exp="" field="dysfunction"/>
    <constraint desc="" exp="" field="remarks"/>
    <constraint desc="" exp="" field="id_model"/>
    <constraint desc="" exp="" field="id_device"/>
    <constraint desc="" exp="" field="id_sensor_type"/>
    <constraint desc="" exp="" field="id_class"/>
    <constraint desc="" exp="" field="id_installation"/>
    <constraint desc="" exp="" field="Periode speciale"/>
  </constraintExpressions>
  <expressionfields>
    <field precision="0" comment="" typeName="text" type="10" length="-1" name="Periode speciale" expression=" check_dates()" subType="0"/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
    <actionsetting id="{458e2ef6-1066-4a7d-8778-163c530bbbb0}" type="1" shortTitle="" name="Exporter la configuration" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" icon="">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{ef45e43b-a0e1-4b80-9681-fa4229ff8bc5}" type="1" shortTitle="" name="Importation" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" icon="">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{d6ede3e2-8e0a-48cf-8e95-40a18956e283}" type="1" shortTitle="" name="Creer un rapport" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" icon="">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{f73c75cf-9fdc-440f-b8ff-52f28335a73f}" type="1" shortTitle="" name="Creer un plan" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" icon="">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{55301a02-ac9f-43c0-9eac-d4f30224254a}" type="1" shortTitle="" name="Générer les graphiques" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" capture="0" isEnabledOnlyWhenEditable="0" notificationMessage="" icon="">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
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
      <column type="actions" hidden="0" width="-1"/>
      <column type="field" hidden="0" name="Periode speciale" width="-1"/>
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
from qgis.utils import plugins

def on_form_open(dialog, layer, feature):
	dialog.widgetValueChanged.connect(partial(on_dialog_changed, dialog))
	
def on_dialog_changed(dialog, attribute, value, attributeChanged):
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
			dialog.changeAttribute('end_process_date', value.addDays(14), '')
			dialog.changeAttribute('Periode speciale', plugins['comptages'].layers.check_dates(value, value.addDays(14)), '')]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="0" name="Periode speciale"/>
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
    <field labelOnTop="0" name="Periode speciale"/>
    <field labelOnTop="0" name="dysfunction"/>
    <field labelOnTop="0" name="end_process_date"/>
    <field labelOnTop="0" name="end_put_date"/>
    <field labelOnTop="0" name="end_service_date"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="id_class"/>
    <field labelOnTop="0" name="id_device"/>
    <field labelOnTop="0" name="id_installation"/>
    <field labelOnTop="0" name="id_model"/>
    <field labelOnTop="0" name="id_sensor_type"/>
    <field labelOnTop="0" name="remarks"/>
    <field labelOnTop="0" name="start_process_date"/>
    <field labelOnTop="0" name="start_put_date"/>
    <field labelOnTop="0" name="start_service_date"/>
    <field labelOnTop="0" name="valid"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
