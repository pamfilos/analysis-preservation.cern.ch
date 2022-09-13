import React from "react";
import PropTypes from "prop-types";
import { Space, Typography, DatePicker } from "antd";
import FacetItem from "./FacetItem";
import RangeSlider from "./Slider";
// import RangeDate from "./RangeDate";
const { RangePicker } = DatePicker;

import queryString from "query-string";

import { withRouter } from "react-router-dom";

const Facet = ({
  category,
  facets,
  isAggSelected,
  selectedAggs,
  onChange,
  history,
}) => {
  const getContentByType = (type) => {
    const choices = {
      range: <RangeSlider items={facets[category]} category={category} />,
      daterange: (
        <RangePicker
          onChange={(d, ds) => {
            if (ds) {
              let params = queryString.parse(history.location.search);
              const location = {
                search: `${queryString.stringify(
                  Object.assign(params, {
                    [category]: `${ds[0]}--${ds[1]}`,
                  })
                )}`,
              };
              history.push(location);
            }
          }}
        />
      ),
      default: (
        <FacetItem
          limit={11}
          items={facets[category].buckets}
          isAggSelected={isAggSelected}
          selectedAggs={selectedAggs}
          onChange={onChange}
          category={category}
        />
      ),
    };

    if (Object.keys(choices).indexOf(type) < 0) type = "default";

    return choices[type];
  };

  const getFacetTitle = (title) =>
    facets[category].meta && facets[category].meta.title
      ? facets[category].meta.title
      : title.replace(/_/g, " ").replace(/\w\S*/g, function (txt) {
          return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });

  return (
    <Space direction="vertical" style={{ width: "100%", marginBottom: "10px" }}>
      <Typography.Title level={5}>{getFacetTitle(category)}</Typography.Title>
      {getContentByType(facets[category].meta && facets[category].meta.type)}
    </Space>
  );
};

Facet.propTypes = {
  category: PropTypes.string,
  facets: PropTypes.object,
  selectedAggs: PropTypes.object,
  onChange: PropTypes.func,
  isAggSelected: PropTypes.func,
};

export default withRouter(Facet);
