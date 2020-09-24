import React from "react";
import PropTypes from "prop-types";

import { connect } from "react-redux";
import { withRouter } from "react-router";

import Box from "grommet/components/Box";
import Sidebar from "grommet/components/Sidebar";

import { toggleFilemanagerLayer } from "../../../actions/draftItem";

import SectionHeader from "./SectionHeader";
import DepositFilesList from "./DepositFilesList";

import { Route } from "react-router-dom";

import TimeAgo from "react-timeago";

import { getBucketById } from "../../../actions/files";

import Tag from "../../partials/Tag";
import Button from "../../partials/Button";
import { AiOutlinePlus, AiOutlineReload } from "react-icons/ai";

class DepositSidebar extends React.Component {
  constructor(props) {
    super(props);
  }

  _renderAddFileIcon() {
    if (this.props.status !== "published") {
      if (this.props.canUpdate) {
        return (
          <Route
            path="/drafts/:draft_id/"
            render={() => (
              <Button
                size="icon"
                icon={<AiOutlinePlus size={20} />}
                onClick={this.props.toggleFilemanagerLayer}
              />
            )}
          />
        );
      }
    }
  }

  _renderRefreshFilesButton() {
    if (this.props.status !== "published") {
      if (this.props.canUpdate) {
        return (
          <Route
            path="/drafts/:draft_id/"
            render={() => (
              <Button
                size="icon"
                onClick={this._refreshFileList}
                icon={<AiOutlineReload size={20} />}
              />
            )}
          />
        );
      }
    }
  }

  _refreshFileList = () => {
    let { bucket } = this.props.links;
    let bucket_id = bucket.split("/").pop();
    this.props.getBucketById(bucket_id);
  };

  _getColorByStatus = status => {
    let colors = {
      draft: {
        bgcolor: "#e6f7ff",
        border: "rgba(0, 106, 147, 1)",
        color: "rgba(0, 106, 147, 1)"
      },
      published: {
        bgcolor: "#f9f0ff",
        border: "rgba(146,109,146,1)",
        color: "rgba(146,109,146,1)"
      }
    };

    return colors[status];
  };
  render() {
    return (
      <Sidebar
        full={false}
        size="medium"
        colorIndex="light-2"
        separator="left"
        className="lg-row"
      >
        <Box flex={false} pad="none" size={{ width: { min: "medium" } }}>
          <Box flex={false} pad="small" style={{ fontWeight: "100" }}>
            <Box
              direction="row"
              wrap={false}
              justify="between"
              margin={{ bottom: "small" }}
              responsive={false}
            >
              ID <span>{this.props.id}</span>
            </Box>

            {
              this.props.schema &&
              <Box
                direction="row"
                wrap={false}
                justify="between"
                margin={{ bottom: "small" }}
                responsive={false}
                align="center"
              >
                <span>Collection</span>
                <Tag
                  text={`${this.props.schema.fullname} v${this.props.schema.version}`}
                />
              </Box>
            }


            <Box
              direction="row"
              wrap={false}
              justify="between"
              margin={{ bottom: "small" }}
              responsive={false}
              align="center"
            >
              <span>Status</span>
              <Tag
                text={this.props.status}
                color={this._getColorByStatus(this.props.status)}
              />
            </Box>

            <Box
              direction="row"
              wrap={false}
              justify="between"
              margin={{ bottom: "small" }}
              responsive={false}
            >
              Creator <span>{this.props.created_by}</span>
            </Box>
            <Box
              direction="row"
              wrap={false}
              justify="between"
              margin={{ bottom: "small" }}
              responsive={false}
            >
              Created:
              {this.props.created && (
                <strong>
                  <TimeAgo date={this.props.created} minPeriod="60" />
                </strong>
              )}
            </Box>
            <Box
              direction="row"
              wrap={false}
              justify="between"
              responsive={false}
            >
              Last Updated:
              {this.props.updated && (
                <strong>
                  <TimeAgo date={this.props.updated} minPeriod="60" />
                </strong>
              )}
            </Box>
          </Box>
        </Box>
        <Box flex={true} pad="none" colorIndex="light-1">
          <SectionHeader
            label="Files | Data | Repos"
            uppercase={true}
            icon={
              <Box
                direction="row"
                responsive={false}
                wrap={false}
                pad={{ between: "small" }}
                margin={{ right: "small" }}
              >
                {this._renderRefreshFilesButton()}
                {this._renderAddFileIcon()}
              </Box>
            }
          />
          <DepositFilesList files={this.props.files} />
        </Box>
      </Sidebar>
    );
  }
}

DepositSidebar.propTypes = {
  toggleFilemanagerLayer: PropTypes.func,
  files: PropTypes.object,
  created_by: PropTypes.string,
  updated: PropTypes.string,
  created: PropTypes.string,
  experiment: PropTypes.string,
  status: PropTypes.string,
  id: PropTypes.string,
  canUpdate: PropTypes.bool,
  links: PropTypes.object,
  getBucketById: PropTypes.func
};

function mapStateToProps(state) {
  return {
    files: state.draftItem.get("bucket"),
    id: state.draftItem.get("id"),
    status: state.draftItem.get("status"),
    schema: state.draftItem.get("schema"),
    experiment: state.draftItem.get("experiment"),
    revision: state.draftItem.get("revision"),
    created_by: state.draftItem.get("created_by"),
    created: state.draftItem.get("created"),
    updated: state.draftItem.get("updated"),
    canUpdate: state.draftItem.get("can_update"),
    links: state.draftItem.get("links")
  };
}

function mapDispatchToProps(dispatch) {
  return {
    toggleFilemanagerLayer: () => dispatch(toggleFilemanagerLayer()),
    getBucketById: bucket_id => dispatch(getBucketById(bucket_id))
  };
}

export default withRouter(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(DepositSidebar)
);
