<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" version="3.20.3-Odense" minScale="1e+08" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal fixedDuration="0" endExpression="" mode="0" startField="start_service_date" startExpression="" accumulate="0" durationUnit="min" enabled="0" durationField="id" endField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option value="id" type="QString" name="dualview/previewExpressions"/>
      <Option value="0" type="QString" name="embeddedWidgets/count"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="id">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="start_service_date">
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
    <field configurationFlags="None" name="end_service_date">
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
    <field configurationFlags="None" name="start_put_date">
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
    <field configurationFlags="None" name="end_put_date">
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
    <field configurationFlags="None" name="start_process_date">
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
    <field configurationFlags="None" name="end_process_date">
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
    <field configurationFlags="None" name="valid">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" type="QString" name="CheckedState"/>
            <Option value="" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dysfunction">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="" type="QString" name="CheckedState"/>
            <Option value="" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="remarks">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id_class">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="Description"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="classification_92fe0fc0_f04c_4ce6_846f_06242ee9b3aa" type="QString" name="Layer"/>
            <Option value="classification" type="QString" name="LayerName"/>
            <Option value="postgres" type="QString" name="LayerProviderName"/>
            <Option value="dbname='comptages' host=localhost port=5432 user='postgres' key='id' checkPrimaryKeyUnicity='1' table=&quot;comptages&quot;.&quot;class&quot;" type="QString" name="LayerSource"/>
            <Option value="1" type="int" name="NofColumns"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id_device">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="automate_28c6e319_528b_40b1_9542_d14a8cd61e65" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id_installation">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="installation_f2dcf353_c673_4919_a24c_7d6ade2cc316" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id_model">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="model_65a6cad5_80d5_4188_8193_26c979000dc6" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id_sensor_type">
      <editWidget type="ValueRelation">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowMulti"/>
            <Option value="false" type="bool" name="AllowNull"/>
            <Option value="" type="QString" name="FilterExpression"/>
            <Option value="id" type="QString" name="Key"/>
            <Option value="type_capteur_34af0101_bcb6_4326_b8e9_059274a30c66" type="QString" name="Layer"/>
            <Option value="false" type="bool" name="OrderByValue"/>
            <Option value="false" type="bool" name="UseCompleter"/>
            <Option value="name" type="QString" name="Value"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="tjm">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Periode speciale">
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
    <alias field="id_class" index="10" name="Classification"/>
    <alias field="id_device" index="11" name="Automate"/>
    <alias field="id_installation" index="12" name="Installation"/>
    <alias field="id_model" index="13" name="Model"/>
    <alias field="id_sensor_type" index="14" name="Type capteur"/>
    <alias field="tjm" index="15" name=""/>
    <alias field="Periode speciale" index="16" name=""/>
  </aliases>
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
    <default field="id_class" applyOnUpdate="0" expression="6"/>
    <default field="id_device" applyOnUpdate="0" expression=""/>
    <default field="id_installation" applyOnUpdate="0" expression="@selected_installation"/>
    <default field="id_model" applyOnUpdate="0" expression=""/>
    <default field="id_sensor_type" applyOnUpdate="0" expression=""/>
    <default field="tjm" applyOnUpdate="0" expression=""/>
    <default field="Periode speciale" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="id" notnull_strength="1" exp_strength="0" constraints="3" unique_strength="1"/>
    <constraint field="start_service_date" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="end_service_date" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="start_put_date" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="end_put_date" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="start_process_date" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="end_process_date" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="valid" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="dysfunction" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="remarks" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="id_class" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="id_device" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="id_installation" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="id_model" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="id_sensor_type" notnull_strength="1" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="tjm" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="Periode speciale" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
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
    <constraint field="id_class" exp="" desc=""/>
    <constraint field="id_device" exp="" desc=""/>
    <constraint field="id_installation" exp="" desc=""/>
    <constraint field="id_model" exp="" desc=""/>
    <constraint field="id_sensor_type" exp="" desc=""/>
    <constraint field="tjm" exp="" desc=""/>
    <constraint field="Periode speciale" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" expression=" check_dates()" precision="0" subType="0" typeName="text" length="-1" name="Periode speciale" type="10"/>
  </expressionfields>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
    <actionsetting icon="" notificationMessage="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_configuration_action([% attribute( $currentfeature, 'id' ) %])" id="{d0ab2fd2-2e43-46fd-91ff-55779d8df0ed}" capture="0" shortTitle="" type="1" name="Exporter la configuration">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" notificationMessage="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_import_single_file_action([% attribute( $currentfeature, 'id' ) %])" id="{e96a12d0-26f6-46a6-93f4-7670a6a95cb2}" capture="0" shortTitle="" type="1" name="Importation">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" notificationMessage="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_report_action([% attribute( $currentfeature, 'id' ) %])" id="{4340a597-9dae-4de3-b713-4a36d39a65b1}" capture="0" shortTitle="" type="1" name="Creer un rapport">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" notificationMessage="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_export_plan_action([% attribute( $currentfeature, 'id' ) %])" id="{7eba486d-2a8a-4394-8320-4167061db6f5}" capture="0" shortTitle="" type="1" name="Creer un plan">
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting icon="" notificationMessage="" isEnabledOnlyWhenEditable="0" action="from qgis.utils import plugins&#xa;plugins['comptages'].do_generate_chart_action([% attribute( $currentfeature, 'id' ) %])" id="{56878393-0746-4771-b326-ee58dc4c6d96}" capture="0" shortTitle="" type="1" name="Générer les graphiques">
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="start_process_date"/>
      <column width="-1" hidden="0" type="field" name="end_process_date"/>
      <column width="-1" hidden="0" type="field" name="start_put_date"/>
      <column width="-1" hidden="0" type="field" name="end_put_date"/>
      <column width="-1" hidden="0" type="field" name="start_service_date"/>
      <column width="-1" hidden="0" type="field" name="end_service_date"/>
      <column width="-1" hidden="0" type="field" name="Periode speciale"/>
      <column width="-1" hidden="0" type="field" name="valid"/>
      <column width="-1" hidden="0" type="field" name="dysfunction"/>
      <column width="-1" hidden="0" type="field" name="remarks"/>
      <column width="-1" hidden="0" type="field" name="id_sensor_type"/>
      <column width="-1" hidden="0" type="field" name="id_class"/>
      <column width="-1" hidden="0" type="field" name="id_model"/>
      <column width="-1" hidden="0" type="field" name="id_device"/>
      <column width="-1" hidden="0" type="field" name="id_installation"/>
      <column width="-1" hidden="0" type="field" name="tjm"/>
      <column width="-1" hidden="0" type="actions"/>
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
    <attributeEditorField showLabel="1" index="5" name="start_process_date"/>
    <attributeEditorField showLabel="1" index="6" name="end_process_date"/>
    <attributeEditorField showLabel="1" index="3" name="start_put_date"/>
    <attributeEditorField showLabel="1" index="4" name="end_put_date"/>
    <attributeEditorField showLabel="1" index="1" name="start_service_date"/>
    <attributeEditorField showLabel="1" index="2" name="end_service_date"/>
    <attributeEditorField showLabel="1" index="16" name="Periode speciale"/>
    <attributeEditorField showLabel="1" index="7" name="valid"/>
    <attributeEditorField showLabel="1" index="8" name="dysfunction"/>
    <attributeEditorField showLabel="1" index="9" name="remarks"/>
    <attributeEditorField showLabel="1" index="14" name="id_sensor_type"/>
    <attributeEditorField showLabel="1" index="10" name="id_class"/>
    <attributeEditorField showLabel="1" index="13" name="id_model"/>
    <attributeEditorField showLabel="1" index="11" name="id_device"/>
    <attributeEditorField showLabel="1" index="12" name="id_installation"/>
    <attributeEditorField showLabel="1" index="17" name="tjm"/>
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
    <field editable="0" name="tjm"/>
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
    <field labelOnTop="0" name="tjm"/>
    <field labelOnTop="0" name="valid"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="Periode speciale"/>
    <field reuseLastValue="0" name="dysfunction"/>
    <field reuseLastValue="0" name="end_process_date"/>
    <field reuseLastValue="0" name="end_put_date"/>
    <field reuseLastValue="0" name="end_service_date"/>
    <field reuseLastValue="0" name="id"/>
    <field reuseLastValue="0" name="id_class"/>
    <field reuseLastValue="0" name="id_device"/>
    <field reuseLastValue="0" name="id_installation"/>
    <field reuseLastValue="0" name="id_model"/>
    <field reuseLastValue="0" name="id_sensor_type"/>
    <field reuseLastValue="0" name="remarks"/>
    <field reuseLastValue="0" name="start_process_date"/>
    <field reuseLastValue="0" name="start_put_date"/>
    <field reuseLastValue="0" name="start_service_date"/>
    <field reuseLastValue="0" name="tjm"/>
    <field reuseLastValue="0" name="valid"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
