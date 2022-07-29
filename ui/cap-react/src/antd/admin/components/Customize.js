import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import PropertyKeyEditorForm from "./PropKeyEditorForm";

import { Card, Space, Tag, Typography } from "antd";

const SIZE_OPTIONS = ["small", "large", "xlarge", "xxlarge", "full"];
const ALIGN_OPTIONS = ["center", "start", "end"];

const Customize = props => {
  const [myPath, setMyPath] = useState([...props._path]);
  const [updateUi, setUpdateUi] = useState(null);
  const [updateSchema, setUpdateSchema] = useState(
    props.schema ? props.schema.toJS() : {}
  );

  //the update for the uiSchema changes
  useEffect(
    () => {
      if (updateUi) {
        props.onUiSchemaChange([...props._uiPath], updateUi);
      }
    },
    [updateUi]
  );

  useEffect(
    () => {
      if (props._path.join(".") != myPath.join(".")) {
        setUpdateSchema(JSON.parse(JSON.stringify(props.schema.toJS())));
        setMyPath([...props._path]);
      }
    },
    [props._path]
  );

  const _onSchemaChange = data => {
    props.onSchemaChange([...props._path], data.formData);
  };
  const _onUiSchemaChange = data => {
    setUpdateUi(data.formData);
  };
  const sizeChange = newSize => {
    if (SIZE_OPTIONS.indexOf(newSize) < 0) return;

    let { uiSchema } = props;
    uiSchema = uiSchema ? uiSchema.toJS() : {};

    let { "ui:options": uiOptions = {}, ...rest } = uiSchema;
    let { size, ...restUIOptions } = uiOptions;

    size = newSize;
    let _uiOptions = { size, ...restUIOptions };

    props.onUiSchemaChange(props.path.get("uiPath").toJS(), {
      ...rest,
      "ui:options": _uiOptions
    });
  };

  const alignChange = newAlign => {
    if (["center", "start", "end"].indexOf(newAlign) < 0) return;

    let { uiSchema } = props;
    uiSchema = uiSchema ? uiSchema.toJS() : {};

    let { "ui:options": uiOptions = {}, ...rest } = uiSchema;
    let { align, ...restUIOptions } = uiOptions;

    align = newAlign;
    let _uiOptions = { align, ...restUIOptions };

    props.onUiSchemaChange(props.path.get("uiPath").toJS(), {
      ...rest,
      "ui:options": _uiOptions
    });
  };

  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      <PropertyKeyEditorForm
        schema={props.schema && props.schema.toJS()}
        uiSchema={props.uiSchema && props.uiSchema.toJS()}
        formData={updateSchema}
        onChange={_onSchemaChange}
        optionsSchemaObject="optionsSchema"
        optionsUiSchemaObject="optionsSchemaUiSchema"
        title="Schema Settings"
      />

      <PropertyKeyEditorForm
        schema={props.schema && props.schema.toJS()}
        uiSchema={props.uiSchema && props.uiSchema.toJS()}
        formData={props.uiSchema && props.uiSchema.toJS()}
        onChange={_onUiSchemaChange}
        optionsSchemaObject="optionsUiSchema"
        optionsUiSchemaObject="optionsUiSchemaUiSchema"
        title="UI Schema Settings"
      />

      {props._path.size == 0 && (
        <Card title="UI Options">
          <Space direction="vertical" size="large" style={{ width: "100%" }}>
            <Space>
              <Typography.Text>Size Options</Typography.Text>
              {SIZE_OPTIONS.map(size => (
                <Tag
                  onClick={() => sizeChange(size)}
                  key={size}
                  color={
                    props.uiSchema &&
                    props.uiSchema.toJS()["ui:options"] &&
                    props.uiSchema.toJS()["ui:options"].size == size &&
                    "geekblue"
                  }
                >
                  {size}
                </Tag>
              ))}
            </Space>
            <Space>
              <Typography.Text>Align Options</Typography.Text>

              {ALIGN_OPTIONS.map(align => (
                <Tag
                  onClick={() => alignChange(align)}
                  key={align}
                  color={
                    props.uiSchema &&
                    props.uiSchema.toJS()["ui:options"] &&
                    props.uiSchema.toJS()["ui:options"].align == align &&
                    "geekblue"
                  }
                >
                  {align}
                </Tag>
              ))}
            </Space>
          </Space>
        </Card>
      )}
    </Space>
  );
};

Customize.propTypes = {
  schema: PropTypes.object,
  uiSchema: PropTypes.object,
  path: PropTypes.object,
  onSchemaChange: PropTypes.func,
  onUiSchemaChange: PropTypes.func,
  _path: PropTypes.object
};

export default Customize;
