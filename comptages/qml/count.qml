<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" version="3.4.3-Madeira" maxScale="0" minScale="1e+08">
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
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="dd-MM-yyyy"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" type="QString" value=""/>
            <Option name="UncheckedState" type="QString" value=""/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" type="QString" value=""/>
            <Option name="UncheckedState" type="QString" value=""/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="true"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"/>
            <Option name="AllowNull" type="bool" value="false"/>
            <Option name="FilterExpression" type="QString" value=""/>
            <Option name="Key" type="QString" value="id"/>
            <Option name="Layer" type="QString" value="model_7d63f4ec_df62_432c_ac6b_27359d1b20e2"/>
            <Option name="OrderByValue" type="bool" value="false"/>
            <Option name="UseCompleter" type="bool" value="false"/>
            <Option name="Value" type="QString" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"/>
            <Option name="AllowNull" type="bool" value="false"/>
            <Option name="FilterExpression" type="QString" value=""/>
            <Option name="Key" type="QString" value="id"/>
            <Option name="Layer" type="QString" value="automate_aa069d1a_9eea_4396_b88e_31fbb23bf84d"/>
            <Option name="OrderByValue" type="bool" value="false"/>
            <Option name="UseCompleter" type="bool" value="false"/>
            <Option name="Value" type="QString" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"/>
            <Option name="AllowNull" type="bool" value="false"/>
            <Option name="FilterExpression" type="QString" value=""/>
            <Option name="Key" type="QString" value="id"/>
            <Option name="Layer" type="QString" value="type_capteur_3750c2dc_fcd8_4007_8c17_2e4c60393572"/>
            <Option name="OrderByValue" type="bool" value="false"/>
            <Option name="UseCompleter" type="bool" value="false"/>
            <Option name="Value" type="QString" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"/>
            <Option name="AllowNull" type="bool" value="false"/>
            <Option name="FilterExpression" type="QString" value=""/>
            <Option name="Key" type="QString" value="id"/>
            <Option name="Layer" type="QString" value="classification_79073d64_2790_44b1_ae0b_3a6ebb8ef88d"/>
            <Option name="OrderByValue" type="bool" value="false"/>
            <Option name="UseCompleter" type="bool" value="false"/>
            <Option name="Value" type="QString" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option name="AllowMulti" type="bool" value="false"/>
            <Option name="AllowNull" type="bool" value="false"/>
            <Option name="FilterExpression" type="QString" value=""/>
            <Option name="Key" type="QString" value="id"/>
            <Option name="Layer" type="QString" value="installation_1a285a06_7b34_474a_bbde_1f6945e89850"/>
            <Option name="OrderByValue" type="bool" value="false"/>
            <Option name="UseCompleter" type="bool" value="false"/>
            <Option name="Value" type="QString" value="name"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Periode speciale">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" name="" index="0"/>
    <alias field="start_service_date" name="Début service" index="1"/>
    <alias field="end_service_date" name="Fin service" index="2"/>
    <alias field="start_put_date" name="Début pose" index="3"/>
    <alias field="end_put_date" name="Fin pose" index="4"/>
    <alias field="start_process_date" name="Début traitement" index="5"/>
    <alias field="end_process_date" name="Fin traitement" index="6"/>
    <alias field="valid" name="Valide" index="7"/>
    <alias field="dysfunction" name="Dysfonctionnement" index="8"/>
    <alias field="remarks" name="Remarques" index="9"/>
    <alias field="id_model" name="Model" index="10"/>
    <alias field="id_device" name="Automate" index="11"/>
    <alias field="id_sensor_type" name="Type capteur" index="12"/>
    <alias field="id_class" name="Classification" index="13"/>
    <alias field="id_installation" name="Installation" index="14"/>
    <alias field="Periode speciale" name="" index="15"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="start_service_date" expression="''" applyOnUpdate="0"/>
    <default field="end_service_date" expression="" applyOnUpdate="0"/>
    <default field="start_put_date" expression="" applyOnUpdate="0"/>
    <default field="end_put_date" expression="" applyOnUpdate="0"/>
    <default field="start_process_date" expression="" applyOnUpdate="0"/>
    <default field="end_process_date" expression="" applyOnUpdate="0"/>
    <default field="valid" expression="" applyOnUpdate="0"/>
    <default field="dysfunction" expression="" applyOnUpdate="0"/>
    <default field="remarks" expression="" applyOnUpdate="0"/>
    <default field="id_model" expression="" applyOnUpdate="0"/>
    <default field="id_device" expression="" applyOnUpdate="0"/>
    <default field="id_sensor_type" expression="" applyOnUpdate="0"/>
    <default field="id_class" expression="" applyOnUpdate="0"/>
    <default field="id_installation" expression="@selected_installation" applyOnUpdate="0"/>
    <default field="Periode speciale" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" notnull_strength="1" exp_strength="0"/>
    <constraint unique_strength="0" field="start_service_date" constraints="1" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" field="end_service_date" constraints="1" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" field="start_put_date" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="end_put_date" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="start_process_date" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="end_process_date" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="valid" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="dysfunction" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="remarks" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="id_model" constraints="1" notnull_strength="1" exp_strength="0"/>
    <constraint unique_strength="0" field="id_device" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="id_sensor_type" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="id_class" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="id_installation" constraints="1" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" field="Periode speciale" constraints="0" notnull_strength="0" exp_strength="0"/>
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
    <constraint field="Periode speciale" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field name="Periode speciale" length="-1" type="10" comment="" typeName="text" expression="' '" subType="0" precision="0"/>
  </expressionfields>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting name="Exporter la configuration" type="1" shortTitle="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" notificationMessage="" icon="" capture="0" id="{398fab98-a6b6-4b89-b8fa-2eed1f31479a}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Importation" type="1" shortTitle="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])" notificationMessage="" icon="" capture="0" id="{56a8c9ab-65d1-4a08-91e0-da2f65ef8508}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Creer un rapport" type="1" shortTitle="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" notificationMessage="" icon="" capture="0" id="{6b61938b-3899-4f57-b7c1-375c356d8350}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Creer un plan" type="1" shortTitle="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" notificationMessage="" icon="" capture="0" id="{afb33b38-5590-442a-8dba-cb2cd82c4e62}">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting name="Générer les graphiques" type="1" shortTitle="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" notificationMessage="" icon="" capture="0" id="{7f722cbf-bb53-4654-884e-d45d9b969342}">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="start_service_date" type="field" hidden="0" width="-1"/>
      <column name="end_service_date" type="field" hidden="0" width="-1"/>
      <column name="start_put_date" type="field" hidden="0" width="-1"/>
      <column name="end_put_date" type="field" hidden="0" width="-1"/>
      <column name="start_process_date" type="field" hidden="0" width="-1"/>
      <column name="end_process_date" type="field" hidden="0" width="-1"/>
      <column name="valid" type="field" hidden="0" width="-1"/>
      <column name="dysfunction" type="field" hidden="0" width="-1"/>
      <column name="remarks" type="field" hidden="0" width="-1"/>
      <column name="id_model" type="field" hidden="0" width="-1"/>
      <column name="id_device" type="field" hidden="0" width="-1"/>
      <column name="id_sensor_type" type="field" hidden="0" width="-1"/>
      <column name="id_class" type="field" hidden="0" width="-1"/>
      <column name="id_installation" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="0" width="-1"/>
      <column name="Periode speciale" type="field" hidden="0" width="-1"/>
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
    <field name="Periode speciale" editable="0"/>
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
    <field name="Periode speciale" labelOnTop="0"/>
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
