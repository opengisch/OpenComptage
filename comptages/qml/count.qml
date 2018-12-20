<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" version="3.2.3-Bonn" maxScale="0" hasScaleBasedVisibilityFlag="0" readOnly="0">
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
            <Option value="model_6d646e9e_731d_457c_8de7_284388786a98" type="QString" name="Layer"/>
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
            <Option value="automate_a652805f_26b3_486e_93a3_0071e0a3c62d" type="QString" name="Layer"/>
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
            <Option value="type_capteur_c867fcee_1803_446d_a8ee_51692c8ffc05" type="QString" name="Layer"/>
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
            <Option value="classification_853a51c4_497d_4ffc_85e2_d2a001b6e43c" type="QString" name="Layer"/>
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
            <Option value="installation_2b7bfb66_024e_4bd6_9663_c59e05444838" type="QString" name="Layer"/>
            <Option value="1" type="int" name="NofColumns"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
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
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" exp_strength="0" notnull_strength="1" constraints="3"/>
    <constraint unique_strength="0" field="start_service_date" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="end_service_date" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="start_put_date" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="end_put_date" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="start_process_date" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="end_process_date" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="valid" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="dysfunction" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="remarks" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="id_model" exp_strength="0" notnull_strength="1" constraints="1"/>
    <constraint unique_strength="0" field="id_device" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="id_sensor_type" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="id_class" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="id_installation" exp_strength="0" notnull_strength="2" constraints="1"/>
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
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
    <actionsetting notificationMessage="" icon="" type="1" name="Exporter la configuration" shortTitle="" isEnabledOnlyWhenEditable="0" capture="0" id="{2c8fa5f7-65a7-4b2d-8d62-53fec2213565}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting notificationMessage="" icon="" type="1" name="Importation" shortTitle="" isEnabledOnlyWhenEditable="0" capture="0" id="{3ad78a1e-e5aa-4196-b7cd-9ec55c4c3b92}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting notificationMessage="" icon="" type="1" name="Creer un rapport" shortTitle="" isEnabledOnlyWhenEditable="0" capture="0" id="{8c0ed9cb-9fc0-471e-b635-9658f9a7ec9d}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting notificationMessage="" icon="" type="1" name="Creer un plan" shortTitle="" isEnabledOnlyWhenEditable="0" capture="0" id="{6736aba5-58ca-4ab6-ac5e-2cd9d22f8138}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting notificationMessage="" icon="" type="1" name="Générer les graphiques" shortTitle="" isEnabledOnlyWhenEditable="0" capture="0" id="{c87ac129-295c-4dbf-ae1d-02d9a28f31ab}" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
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
			dialog.changeAttribute('end_service_date', value.addDays(7), '')
			dialog.changeAttribute('start_put_date', value, '')
			dialog.changeAttribute('end_put_date', value.addDays(7), '')
			dialog.changeAttribute('start_process_date', value, '')
			dialog.changeAttribute('end_process_date', value.addDays(7), '')
		if attribute == 'start_put_date':
			dialog.changeAttribute('end_put_date', value.addDays(7), '')
		if attribute == 'start_process_date':
			dialog.changeAttribute('end_process_date', value.addDays(7), '')]]></editforminitcode>
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
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
