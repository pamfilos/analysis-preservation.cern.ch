import React from "react";
import PropTypes from "prop-types";

import FormField from "grommet/components/FormField";
import Box from "grommet/components/Box";

let FieldTemplate = function(props) {
  const { id, label, rawDescription, rawErrors = [], children } = props;
  let _errors = "";

  if (rawErrors.length > 0)
    rawErrors.map((error, index) => {
      _errors += `(${index + 1}) ${error} `;
    });

  if (id == "root") {
    switch (props.uiSchema["layout"]) {
      case "full":
        return <Box size="medium">{children}</Box>;
      default:
        // return <Box size="medium">{children}</Box>;
        return (
          <Box
            size="medium"
            flex="grow"
            justify="center"
            alignSelf="center"
            wrap={false}
          >
            {children}
          </Box>
        );
    }
  }
  if (["array", "object"].indexOf(props.schema.type) > -1) {
    return (
      <Box
        style={{
          borderLeft: rawErrors.length > 0 ? "2px #F04B37 solid" : null
        }}
      >
        {children}
      </Box>
    );
  }

  return (
    <FormField
      label={
        <span>
          <span style={{ color: "#000" }}>{label}</span>
          {rawDescription ? (
            <span style={{ color: "#bbb" }}> &nbsp; {rawDescription}</span>
          ) : null}
        </span>
      }
      key={id + label}
      error={rawErrors.length > 0 ? _errors : null}
    >
      {children}
    </FormField>
  );
};

FieldTemplate.propTypes = {
  id: PropTypes.string,
  label: PropTypes.string,
  rawDescription: PropTypes.string,
  rawErrors: PropTypes.array,
  schema: PropTypes.object,
  children: PropTypes.element
};

export default FieldTemplate;
