import React from "react";
import PropTypes from "prop-types";

import { connect } from "react-redux";

import Box from "grommet/components/Box";

import Paragraph from "grommet/components/Paragraph";

import equal from "deep-equal";
import cleanDeep from "clean-deep";

import Notification from "../../partials/Notification";
import Button from "../../partials/Button";
import Modal from "../../partials/Modal";

import {
  publishDraft,
  discardDraft,
  deleteDraft,
  toggleActionsLayer,
  updateDraft
  // togglePreviewer
} from "../../../actions/draftItem";

class DraftActionsLayer extends React.Component {
  renderAction(action) {
    switch (action) {
      // case "save":
      //   this.props.saveData();
      //   this.props.toggleActionsLayer();
      //   break;
      case "publish":
        equal(cleanDeep(this.props.formData), cleanDeep(this.props.metadata))
          ? this.props.publishDraft(this.props.draft_id)
          : this.props
              .updateDraft({ ...this.props.formData }, this.props.draft_id)
              .then(() => {
                this.props.publishDraft(this.props.draft_id);
              });
        this.props.toggleActionsLayer();
        break;
      case "delete":
        this.props.deleteDraft(this.props.draft_id);
        this.props.toggleActionsLayer();
        break;
      case "discard":
        this.props.discardDraft(this.props.draft_id);
        this.props.toggleActionsLayer();
        break;
    }
  }

  getTitle = title => {
    const choices = {
      delete: "Delete",
      publish: "Publish",
      discard: "Discard",
      save: "Save"
    };

    return choices[title];
  };

  renderMessage(action) {
    switch (action) {
      // case "save":
      //   return (
      //     <Paragraph>Are you sure you want to save your changes?</Paragraph>
      //   );
      case "publish":
        return (
          <div>
            {!equal(cleanDeep(this.props.formData), cleanDeep(this.props.metadata)) && (
              <Notification
                type="warning"
                text="Your analysis has unsaved changes. If you continue these changes will be saved and published."
              />
            )}
            <Paragraph>
              You will now create a <strong>new published version</strong>
            </Paragraph>
            <Paragraph>
              Your published record will be visible to <strong>all members of the collaboration</strong>.
            </Paragraph>
          </div>
        );
      case "delete":
        return (
          <Paragraph>
            This will <b>permanently</b> delete this analysis and all related
            data (<b>including files and workflows</b>).<br />
            <br />
            Already published versions of the analysis <b>will not</b> be
            affected.<br />
            <br />
            <b>Are you sure you want to delete this draft?</b>{" "}
          </Paragraph>
        );
      case "discard":
        return (
          <Paragraph>
            Discard changes to the previous published version?
          </Paragraph>
        );
    }
  }

  render() {
    return this.props.actionsLayer ? (
      <Modal
        title={this.getTitle(this.props.type)}
        Tag="h4"
        onClose={this.props.toggleActionsLayer}
        separator
      >
        <Box
          justify="center"
          flex={true}
          wrap={false}
          pad={{ horizontal: "small" }}
          size="medium"
        >
          <Box pad={{ horizontal: "small" }} alignContent="center">
            {this.renderMessage(this.props.type)}
          </Box>
          <Box
            direction="row"
            responsive={false}
            justify="between"
            align="center"
            pad={{ horizontal: "small" }}
          >
            <Button
              text="Cancel"
              secondary
              onClick={() => this.props.toggleActionsLayer()}
            />

            <Button
              text={
                this.props.type.charAt(0).toUpperCase() +
                this.props.type.slice(1)
              }
              primaryPublished
              critical={this.props.type === "delete"}
              onClick={() => this.renderAction(this.props.type)}
            />
          </Box>
        </Box>
      </Modal>
    ) : null;
  }
}

DraftActionsLayer.propTypes = {
  actionsLayer: PropTypes.bool,
  schemaId: PropTypes.object,
  // saveData: PropTypes.func,
  publishData: PropTypes.func,
  deleteDraft: PropTypes.func,
  discardData: PropTypes.func,
  type: PropTypes.string,
  toggleActionsLayer: PropTypes.func,
  publishDraft: PropTypes.func,
  discardDraft: PropTypes.func,
  draft_id: PropTypes.string,
  updateDraft: PropTypes.func,
  formData: PropTypes.object,
  metadata: PropTypes.object
};

function mapStateToProps(state) {
  return {
    actionsLayer: state.draftItem.get("actionsLayer"),
    type: state.draftItem.get("actionsLayerType"),
    draft_id: state.draftItem.get("id"),
    formData: state.draftItem.get("formData"),
    metadata: state.draftItem.get("metadata")
  };
}

function mapDispatchToProps(dispatch) {
  return {
    toggleActionsLayer: () => dispatch(toggleActionsLayer()),
    publishDraft: draft_id => dispatch(publishDraft(draft_id)),
    deleteDraft: draft_id => dispatch(deleteDraft(draft_id)),
    discardDraft: draft_id => dispatch(discardDraft(draft_id)),
    updateDraft: (data, draft_id) => dispatch(updateDraft(data, draft_id))
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftActionsLayer);
