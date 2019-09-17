const simple = {
  string: {
    title: "Text",
    description: "Titles, names, paragraphs, IDs, list of names",
    child: {},
    default: {
      schema: {
        type: "string"
      },
      uiSchema: {}
    }
  },
  number: {
    title: "Number",
    description: "IDs, order number, rating, quantity",
    child: {},
    default: {
      schema: {
        type: "number"
      },
      uiSchema: {}
    }
  },
  object: {
    title: "JSON Object",
    description: "Data in JSON format, Grouped section",
    child: {},
    default: {
      schema: {
        type: "object",
        properties: {}
      },
      uiSchema: {}
    }
  },
  reference: {
    title: "Reference",
    description: "For example, an analysis can reference its author(s)",
    child: {},
    default: {
      schema: {
        type: "string"
      },
      uiSchema: {}
    }
  },
  boolean: {
    title: "Boolean",
    description: "Yes or no, 1 or 0, true or false",
    child: {},
    default: {
      schema: {
        type: "boolean",
        properties: {}
      },
      uiSchema: {}
    }
  },
  array: {
    title: "Array",
    description:
      "A list of things. List of strings, numbers, objects, references",
    child: {},
    default: {
      schema: {
        type: "array",
        items: {}
      },
      uiSchema: {}
    }
  }
};

const advanced = {
  accordion: {
    title: "Accordion",
    description: "Data in JSON format, Grouped section",
    child: {},
    default: {
      schema: {
        type: "object",
        properties: {}
      },
      uiSchema: {
        "ui:object": "accordionObjectField"
      }
    }
  }
};

const fields = {
  advanced: {
    title: "Advanced Fields",
    description: "",
    fields: advanced
  },
  simple: {
    title: "Simple Fields",
    description: "",
    fields: simple
  }
};

export default fields;
