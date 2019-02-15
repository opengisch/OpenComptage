<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" maxScale="0" version="3.4.3-Madeira" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="id" key="dualview/previewExpressions"/>
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
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_service_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_put_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="end_process_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="allow_null"/>
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="dd-MM-yyyy" name="display_format"/>
            <Option type="QString" value="yyyy-MM-dd" name="field_format"/>
            <Option type="bool" value="false" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" value="" name="CheckedState"/>
            <Option type="QString" value="" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" value="" name="CheckedState"/>
            <Option type="QString" value="" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="false" name="AllowNull"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="id" name="Key"/>
            <Option type="QString" value="model_9ba4dedb_f693_4f18_bf33_e9438fe96381" name="Layer"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="name" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="false" name="AllowNull"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="id" name="Key"/>
            <Option type="QString" value="automate_d41b1b3f_ad04_4a11_a33d_80a90153fae1" name="Layer"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="name" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="false" name="AllowNull"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="id" name="Key"/>
            <Option type="QString" value="type_capteur_5b0b9c94_c5ea_4217_80df_35148790cc52" name="Layer"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="name" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="true" name="AllowNull"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="id" name="Key"/>
            <Option type="QString" value="classification_8a8da63d_8977_4713_9258_51c3e1308224" name="Layer"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="name" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="AllowMulti"/>
            <Option type="bool" value="false" name="AllowNull"/>
            <Option type="QString" value="" name="FilterExpression"/>
            <Option type="QString" value="id" name="Key"/>
            <Option type="QString" value="installation_c31ea9e0_3620_4919_845f_1eaba6361895" name="Layer"/>
            <Option type="bool" value="false" name="OrderByValue"/>
            <Option type="bool" value="false" name="UseCompleter"/>
            <Option type="QString" value="name" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Periode speciale">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
    <alias index="15" name="" field="Periode speciale"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="''" field="start_service_date" applyOnUpdate="0"/>
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
    <default expression="" field="Periode speciale" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1" field="id"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="start_service_date"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="end_service_date"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="start_put_date"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="end_put_date"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="start_process_date"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="end_process_date"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="valid"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="dysfunction"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="remarks"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="id_model"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="id_device"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="id_sensor_type"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="id_class"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="1" unique_strength="0" field="id_installation"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0" field="Periode speciale"/>
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
    <field type="10" expression=" check_dates()" subType="0" name="Periode speciale" typeName="text" length="-1" precision="0" comment=""/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
    <actionsetting type="1" notificationMessage="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" id="{ca6b2377-6ff6-40a6-904c-3c49b3c6c301}" shortTitle="" icon="" capture="0" name="Exporter la configuration" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" notificationMessage="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])" id="{e50bc99e-2f48-4e31-bae8-1e999f80a79e}" shortTitle="" icon="" capture="0" name="Importation" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" notificationMessage="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" id="{da14a4fa-31fa-40b4-85b4-f3d835f7f996}" shortTitle="" icon="" capture="0" name="Creer un rapport" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" notificationMessage="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" id="{fe2069f6-0dd8-4085-8279-498cebe8013a}" shortTitle="" icon="" capture="0" name="Creer un plan" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting type="1" notificationMessage="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" id="{8246e6be-34c0-4b4a-8514-a5ed7c0eef42}" shortTitle="" icon="" capture="0" name="Générer les graphiques" isEnabledOnlyWhenEditable="0">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column type="field" width="-1" hidden="0" name="id"/>
      <column type="field" width="-1" hidden="0" name="start_service_date"/>
      <column type="field" width="-1" hidden="0" name="end_service_date"/>
      <column type="field" width="-1" hidden="0" name="start_put_date"/>
      <column type="field" width="-1" hidden="0" name="end_put_date"/>
      <column type="field" width="-1" hidden="0" name="start_process_date"/>
      <column type="field" width="-1" hidden="0" name="end_process_date"/>
      <column type="field" width="-1" hidden="0" name="valid"/>
      <column type="field" width="-1" hidden="0" name="dysfunction"/>
      <column type="field" width="-1" hidden="0" name="remarks"/>
      <column type="field" width="-1" hidden="0" name="id_model"/>
      <column type="field" width="-1" hidden="0" name="id_device"/>
      <column type="field" width="-1" hidden="0" name="id_sensor_type"/>
      <column type="field" width="-1" hidden="0" name="id_class"/>
      <column type="field" width="-1" hidden="0" name="id_installation"/>
      <column type="actions" width="-1" hidden="0"/>
      <column type="field" width="-1" hidden="0" name="Periode speciale"/>
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
		if attribute == 'start_process_date':
			dialog.changeAttribute('end_process_date', value.addDays(13), '')
			dialog.changeAttribute('start_put_date', value.addDays(-4), '')
			dialog.changeAttribute('end_put_date', value.addDays(14), '')
			dialog.changeAttribute('start_service_date', value.addDays(-5), '')
			dialog.changeAttribute('end_service_date', value.addDays(15), '')            
			dialog.changeAttribute('Periode speciale', plugins['comptages'].layers.check_dates(value, value.addDays(13)), '')]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorField index="5" name="start_process_date" showLabel="1"/>
    <attributeEditorField index="6" name="end_process_date" showLabel="1"/>
    <attributeEditorField index="3" name="start_put_date" showLabel="1"/>
    <attributeEditorField index="4" name="end_put_date" showLabel="1"/>
    <attributeEditorField index="1" name="start_service_date" showLabel="1"/>
    <attributeEditorField index="2" name="end_service_date" showLabel="1"/>
    <attributeEditorField index="15" name="Periode speciale" showLabel="1"/>
    <attributeEditorField index="7" name="valid" showLabel="1"/>
    <attributeEditorField index="8" name="dysfunction" showLabel="1"/>
    <attributeEditorField index="9" name="remarks" showLabel="1"/>
    <attributeEditorField index="12" name="id_sensor_type" showLabel="1"/>
    <attributeEditorField index="13" name="id_class" showLabel="1"/>
    <attributeEditorField index="10" name="id_model" showLabel="1"/>
    <attributeEditorField index="11" name="id_device" showLabel="1"/>
    <attributeEditorField index="14" name="id_installation" showLabel="1"/>
  </attributeEditorForm>
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
