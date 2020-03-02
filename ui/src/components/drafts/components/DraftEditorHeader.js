import React from "react";
import PropTypes from "prop-types";

import { connect } from "react-redux";
import cogoToast from "cogo-toast";
import _isEmpty from "lodash/isEmpty";

import Box from "grommet/components/Box";
import Menu from "grommet/components/Menu";
import Spinning from "grommet/components/icons/Spinning";

import { SaveAnchor, DraftMessage } from "./Buttons";

import {
  createDraft,
  createDraftError,
  updateDraft,
  editPublished,
  toggleActionsLayer
  // togglePreviewer
} from "../../../actions/draftItem";
import { withRouter } from "react-router";

class DraftEditorHeader extends React.Component {
  _validateFormData = () => {
    // TOFIX maybe fetch formData from store instead of ref
    const formData = this.props.formRef.current
      ? this.props.formRef.current.props.formData
      : null;

    // let {
    //   "current": {
    //     props: {
    //       "formData": formData = null,
    //     } = {},
    //     "validate": validate = null
    //   } = {}
    // } =  this.props.formRef;

    // const { errors = []} = this.props.formRef.current && this.props.formRef.current.validate(formData);

    const { errors } = this.props.formRef.current.validate(formData);

    this.props.formRef.current.submit();

    let emptyObject = 0;

    Object.values(formData).map(formItem => {
      if (_isEmpty(formItem)) {
        emptyObject++;
      } else {
        Object.values(formItem).map(value => {
          if (_isEmpty(value)) {
            emptyObject++;
          }
        });
      }
    });

    let condition =
      _isEmpty(formData) || emptyObject === Object.entries(formData).length;

    if (errors.length > 0) {
      cogoToast.error("Make sure all the fields are properly filled in", {
        position: "top-center",
        heading: "Form could not be submitted",
        bar: { size: "0" },
        hideAfter: 5
      });
      return false;
    }

    if (condition) {
      cogoToast.warn(
        "Please add some content first, and try again saving again",
        {
          position: "top-center",
          heading: "Form is empty",
          bar: { size: "0" },
          hideAfter: 3
        }
      );
      return false;
    } else {
      return true;
    }
  };

  _createDraft = schema_id => {
    if (this._validateFormData()) {
      this.props.createDraft(this.props.formData, schema_id).finally(() => {
        this._validateFormData();
      });
    }
  };

  _saveData() {
    if (this._validateFormData()) {
      let status = this.props.status;
      if (status == "draft") {
        this.props
          .updateDraft({ ...this.props.formData }, this.props.draft_id)
          .finally(() => {
            this._validateFormData();
          });
      } else if (status == "published")
        this.props
          .editPublished(
            { ...this.props.formData, $schema: this.props.draft.$schema },
            this.props.match.params.schema_id,
            this.props.draft_id
          )
          .finally(() => {
            this._validateFormData();
          });
    }
  }

  _actionHandler = type => () => {
    this.props.toggleActionsLayer(type);
  };

  render() {
    // let status = this.props.status;

    // let isDraft = status == "draft" ? true : false;
    // let isPublishedOnce = this.props.recid ? true : false;

    // ******** NEEDED
    // if (
    //   (this.props.errors && this.props.error.status == 403) ||
    //   (this.props.schemaError && this.props.schemaError.status == 403)
    // )
    //   return null;
    if (this.props.schemaErrors.length > 0) {
      return null;
    }

    return (
      <Box flex={true} wrap={false} direction="row">
        <Box flex={true} justify="center" align="end">
          <DraftMessage
            key="draft-message"
            message={this.props.message}
            loading={this.props.loading}
          />
        </Box>
        <Box flex={false} direction="row" wrap={false} justify="end">
          {this.props.loading ? (
            <Box
              flex={true}
              direction="row"
              align="center"
              margin={{ horizontal: "small" }}
            >
              <Spinning />
            </Box>
          ) : null}

          {this.props.draft_id && (
            <Menu
              flex={false}
              direction="row"
              wrap={false}
              responsive={false}
              size="small"
              pad={{ horizontal: "small" }}
              alignContent="center"
              justify="center"
              align="center"
            >
              {/*
                isDraft && isPublishedOnce ? (
                  <DiscardAnchor action={this._actionHandler("discard")} />
                ) : null
              */}

              <SaveAnchor action={this._saveData.bind(this)} />
            </Menu>
          )}
        </Box>
      </Box>
    );
  }
}

DraftEditorHeader.propTypes = {
  match: PropTypes.object.isRequired,
  draft: PropTypes.object,
  id: PropTypes.string,
  formRef: PropTypes.object,
  message: PropTypes.string,
  loading: PropTypes.bool,
  schemaErrors: PropTypes.array,
  discardDraft: PropTypes.func,
  updateDraft: PropTypes.func,
  editPublished: PropTypes.func,
  createDraft: PropTypes.func,
  publishDraft: PropTypes.func,
  formData: PropTypes.object,
  toggleActionsLayer: PropTypes.func,
  deleteDraft: PropTypes.func,
  schema: PropTypes.object,
  status: PropTypes.string,
  draft_id: PropTypes.string,
  recid: PropTypes.string
};

function mapStateToProps(state) {
  return {
    draft_id: state.draftItem.get("id"),
    recid: state.draftItem.get("recid"),
    draft: state.draftItem.get("metadata"),
    schema: state.draftItem.get("schema"),
    status: state.draftItem.get("status"),
    // schema: state.draftItem.getIn(["current_item", "schema"]),
    formData: state.draftItem.get("formData"),
    // depositGroups: state.auth.getIn(["currentUser", "depositGroups"]),
    errors: state.draftItem.get("errors"),
    schemaErrors: state.draftItem.get("schemaErrors"),
    loading: state.draftItem.get("loading")
    // loading: state.draftItem.getIn(["current_item", "loading"]),
    // message: state.drafts.getIn(["current_item", "message"])
  };
}

function mapDispatchToProps(dispatch) {
  return {
    createDraft: (data, ana_type) => dispatch(createDraft(data, ana_type)),
    createDraftError: err => dispatch(createDraftError(err)),
    updateDraft: (data, draft_id) => dispatch(updateDraft(data, draft_id)),
    editPublished: (data, schema, draft_id) =>
      dispatch(editPublished(data, schema, draft_id)),
    toggleActionsLayer: type => dispatch(toggleActionsLayer(type))
  };
}

export default withRouter(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(DraftEditorHeader)
);
