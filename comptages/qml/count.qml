<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" readOnly="0" maxScale="0" version="3.18.0-Zürich">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal startField="start_service_date" startExpression="" fixedDuration="0" endField="start_service_date" mode="0" durationUnit="min" accumulate="0" durationField="" enabled="0" endExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_service_date" configurationFlags="None">
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
    <field name="end_service_date" configurationFlags="None">
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
    <field name="start_put_date" configurationFlags="None">
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
    <field name="end_put_date" configurationFlags="None">
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
    <field name="start_process_date" configurationFlags="None">
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
    <field name="end_process_date" configurationFlags="None">
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
    <field name="valid" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" name="CheckedState" type="QString"/>
            <Option value="" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dysfunction" configurationFlags="None">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" name="CheckedState" type="QString"/>
            <Option value="" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="remarks" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_model" configurationFlags="None">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="model_4bf3cb19_9e02_44e3_9f29_138e71ca3ca9" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_device" configurationFlags="None">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="automate_d9f7513c_e57a_4b57_b512_f7325a0d9d5e" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_sensor_type" configurationFlags="None">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="type_capteur_2cff0d98_bfae_438d_b3b9_52502d56df31" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_class" configurationFlags="None">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="classification_1c5e9108_9a00_4e46_9082_0ecccd0834c0" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_installation" configurationFlags="None">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" name="AllowMulti" type="bool"/>
            <Option value="false" name="AllowNull" type="bool"/>
            <Option value="" name="FilterExpression" type="QString"/>
            <Option value="id" name="Key" type="QString"/>
            <Option value="installation_b3946f2d_dd60_439f_ae4d_e75b774eb45e" name="Layer" type="QString"/>
            <Option value="false" name="OrderByValue" type="bool"/>
            <Option value="false" name="UseCompleter" type="bool"/>
            <Option value="name" name="Value" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Periode speciale" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
    <constraint constraints="3" exp_strength="0" unique_strength="1" notnull_strength="1" field="id"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="start_service_date"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="end_service_date"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="start_put_date"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="end_put_date"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="start_process_date"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="end_process_date"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="valid"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="dysfunction"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="remarks"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="id_model"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="id_device"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="id_sensor_type"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="id_class"/>
    <constraint constraints="1" exp_strength="0" unique_strength="0" notnull_strength="1" field="id_installation"/>
    <constraint constraints="0" exp_strength="0" unique_strength="0" notnull_strength="0" field="Periode speciale"/>
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
    <constraint desc="" field="Periode speciale" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field expression=" check_dates()" precision="0" length="-1" comment="" name="Periode speciale" typeName="text" subType="0" type="10"/>
  </expressionfields>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting id="{5d35b527-d57d-4e78-b992-c5814af56236}" icon="" isEnabledOnlyWhenEditable="0" name="Exporter la configuration" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% $id %])" notificationMessage="" type="1" capture="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{9696ea9a-5aba-4f4a-9e25-142843c6c46e}" icon="" isEnabledOnlyWhenEditable="0" name="Importation" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% $id %])" notificationMessage="" type="1" capture="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{e8176c7e-aec9-442f-af02-ac2d5c7850b6}" icon="" isEnabledOnlyWhenEditable="0" name="Creer un rapport" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% $id %])" notificationMessage="" type="1" capture="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{52540539-d3c3-4be0-9dbb-a9d926c0eb30}" icon="" isEnabledOnlyWhenEditable="0" name="Creer un plan" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% $id %])" notificationMessage="" type="1" capture="0">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting id="{9fc06872-25d7-4dda-a7f1-167587905505}" icon="" isEnabledOnlyWhenEditable="0" name="Générer les graphiques" shortTitle="" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% $id %])" notificationMessage="" type="1" capture="0">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="id" hidden="0" width="-1" type="field"/>
      <column name="start_service_date" hidden="0" width="-1" type="field"/>
      <column name="end_service_date" hidden="0" width="-1" type="field"/>
      <column name="start_put_date" hidden="0" width="-1" type="field"/>
      <column name="end_put_date" hidden="0" width="-1" type="field"/>
      <column name="start_process_date" hidden="0" width="-1" type="field"/>
      <column name="end_process_date" hidden="0" width="-1" type="field"/>
      <column name="valid" hidden="0" width="-1" type="field"/>
      <column name="dysfunction" hidden="0" width="-1" type="field"/>
      <column name="remarks" hidden="0" width="-1" type="field"/>
      <column name="id_model" hidden="0" width="-1" type="field"/>
      <column name="id_device" hidden="0" width="-1" type="field"/>
      <column name="id_sensor_type" hidden="0" width="-1" type="field"/>
      <column name="id_class" hidden="0" width="-1" type="field"/>
      <column name="id_installation" hidden="0" width="-1" type="field"/>
      <column hidden="0" width="-1" type="actions"/>
      <column name="Periode speciale" hidden="0" width="-1" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
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
    dialog.changeAttribute('id_class', 6)

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
    <attributeEditorField showLabel="1" name="start_process_date" index="5"/>
    <attributeEditorField showLabel="1" name="end_process_date" index="6"/>
    <attributeEditorField showLabel="1" name="start_put_date" index="3"/>
    <attributeEditorField showLabel="1" name="end_put_date" index="4"/>
    <attributeEditorField showLabel="1" name="start_service_date" index="1"/>
    <attributeEditorField showLabel="1" name="end_service_date" index="2"/>
    <attributeEditorField showLabel="1" name="Periode speciale" index="15"/>
    <attributeEditorField showLabel="1" name="valid" index="7"/>
    <attributeEditorField showLabel="1" name="dysfunction" index="8"/>
    <attributeEditorField showLabel="1" name="remarks" index="9"/>
    <attributeEditorField showLabel="1" name="id_sensor_type" index="12"/>
    <attributeEditorField showLabel="1" name="id_class" index="13"/>
    <attributeEditorField showLabel="1" name="id_model" index="10"/>
    <attributeEditorField showLabel="1" name="id_device" index="11"/>
    <attributeEditorField showLabel="1" name="id_installation" index="14"/>
  </attributeEditorForm>
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
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
