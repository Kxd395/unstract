import {
  CheckCircleOutlined,
  DeleteOutlined,
  EditOutlined,
  LoadingOutlined,
  PlayCircleFilled,
  PlayCircleOutlined,
  SyncOutlined,
} from "@ant-design/icons";
import { useState } from "react";
import { Button, Checkbox, Col, Divider, Row, Tag, Tooltip } from "antd";
import PropTypes from "prop-types";

import { promptStudioUpdateStatus } from "../../../helpers/GetStaticData";
import { ConfirmModal } from "../../widgets/confirm-modal/ConfirmModal";
import { EditableText } from "../editable-text/EditableText";
import { useCustomToolStore } from "../../../store/custom-tool-store";
import { ExpandCardBtn } from "./ExpandCardBtn";

let PromptRunBtnSps;
try {
  PromptRunBtnSps =
    require("../../../plugins/simple-prompt-studio/PromptRunBtnSps").PromptRunBtnSps;
} catch {
  // The component will remain 'undefined' it is not available
}

function Header({
  promptDetails,
  promptKey,
  setPromptKey,
  progressMsg,
  handleRun,
  handleChange,
  handleDelete,
  updateStatus,
  updatePlaceHolder,
  isCoverageLoading,
  isEditingTitle,
  setIsEditingTitle,
  enableEdit,
  expandCard,
  setExpandCard,
  enabledProfiles,
  spsLoading,
  handleSpsLoading,
  handleGetOutput,
}) {
  const {
    selectedDoc,
    disableLlmOrDocChange,
    singlePassExtractMode,
    isSinglePassExtractLoading,
    indexDocs,
    isPublicSource,
    isSimplePromptStudio,
  } = useCustomToolStore();

  const [isDisablePrompt, setIsDisablePrompt] = useState(promptDetails?.active);

  const handleRunBtnClick = (profileManager = null, coverAllDoc = true) => {
    setExpandCard(true);
    handleRun(profileManager, coverAllDoc, enabledProfiles, true);
  };

  const handleDisablePrompt = (event) => {
    const check = event?.target?.checked;
    setIsDisablePrompt(check);
    handleChange(check, promptDetails?.prompt_id, "active", true, true).catch(
      () => {
        setIsDisablePrompt(!check);
      }
    );
  };

  return (
    <Row>
      <Col span={12}>
        <EditableText
          isEditing={isEditingTitle}
          setIsEditing={setIsEditingTitle}
          text={promptKey}
          setText={setPromptKey}
          promptId={promptDetails?.prompt_id}
          defaultText={promptDetails?.prompt_key}
          handleChange={handleChange}
          placeHolder={updatePlaceHolder}
        />
      </Col>
      <Col span={12} className="display-flex-right">
        {progressMsg?.message && (
          <Tooltip title={progressMsg?.message || ""}>
            <Tag
              icon={isCoverageLoading && <LoadingOutlined spin />}
              color={progressMsg?.level === "ERROR" ? "error" : "processing"}
              className="display-flex-align-center"
            >
              <div className="tag-max-width ellipsis">
                {progressMsg?.message}
              </div>
            </Tag>
          </Tooltip>
        )}
        {updateStatus?.promptId === promptDetails?.prompt_id && (
          <>
            {updateStatus?.status === promptStudioUpdateStatus.isUpdating && (
              <Tag
                icon={<SyncOutlined spin />}
                color="processing"
                className="display-flex-align-center"
              >
                Updating
              </Tag>
            )}
            {updateStatus?.status === promptStudioUpdateStatus.done && (
              <Tag
                icon={<CheckCircleOutlined />}
                color="success"
                className="display-flex-align-center"
              >
                Done
              </Tag>
            )}
            {updateStatus?.status ===
              promptStudioUpdateStatus.validationError && (
              <Tag
                icon={<CheckCircleOutlined />}
                color="error"
                className="display-flex-align-center"
              >
                Invalid JSON Key
              </Tag>
            )}
          </>
        )}
        <ExpandCardBtn expandCard={expandCard} setExpandCard={setExpandCard} />
        <Tooltip title="Edit">
          <Button
            size="small"
            type="text"
            className="prompt-card-action-button"
            onClick={enableEdit}
            disabled={
              disableLlmOrDocChange.includes(promptDetails?.prompt_id) ||
              isSinglePassExtractLoading ||
              spsLoading[selectedDoc?.document_id] ||
              indexDocs.includes(selectedDoc?.document_id) ||
              isPublicSource
            }
          >
            <EditOutlined className="prompt-card-actions-head" />
          </Button>
        </Tooltip>
        {!singlePassExtractMode && !isSimplePromptStudio && (
          <>
            <Tooltip title="Run">
              <Button
                size="small"
                type="text"
                className="prompt-card-action-button"
                onClick={() =>
                  handleRunBtnClick(promptDetails?.profile_manager, false)
                }
                disabled={
                  (updateStatus?.promptId === promptDetails?.prompt_id &&
                    updateStatus?.status ===
                      promptStudioUpdateStatus?.isUpdating) ||
                  disableLlmOrDocChange?.includes(promptDetails?.prompt_id) ||
                  indexDocs?.includes(selectedDoc?.document_id) ||
                  isPublicSource ||
                  spsLoading[selectedDoc?.document_id]
                }
              >
                <PlayCircleOutlined className="prompt-card-actions-head" />
              </Button>
            </Tooltip>
            <Tooltip title="Run All">
              <Button
                size="small"
                type="text"
                className="prompt-card-action-button"
                onClick={handleRunBtnClick}
                disabled={
                  (updateStatus?.promptId === promptDetails?.prompt_id &&
                    updateStatus?.status ===
                      promptStudioUpdateStatus?.isUpdating) ||
                  disableLlmOrDocChange?.includes(promptDetails?.prompt_id) ||
                  indexDocs?.includes(selectedDoc?.document_id) ||
                  isPublicSource
                }
              >
                <PlayCircleFilled className="prompt-card-actions-head" />
              </Button>
            </Tooltip>
          </>
        )}
        {isSimplePromptStudio && PromptRunBtnSps && (
          <PromptRunBtnSps
            spsLoading={spsLoading}
            handleSpsLoading={handleSpsLoading}
            handleGetOutput={handleGetOutput}
            promptDetails={promptDetails}
          />
        )}
        {!isSimplePromptStudio && (
          <Tooltip title={isDisablePrompt ? "Disable Prompt" : "Enable Prompt"}>
            <Checkbox
              checked={isDisablePrompt}
              className="prompt-card-action-button"
              onChange={handleDisablePrompt}
            />
          </Tooltip>
        )}
        <Divider type="vertical" className="header-delete-divider" />
        <ConfirmModal
          handleConfirm={() => handleDelete(promptDetails?.prompt_id)}
          content="The prompt will be permanently deleted."
        >
          <Tooltip title="Delete">
            <Button
              size="small"
              type="text"
              className="prompt-card-action-button"
              disabled={
                disableLlmOrDocChange?.includes(promptDetails?.prompt_id) ||
                isSinglePassExtractLoading ||
                indexDocs?.includes(selectedDoc?.document_id) ||
                isPublicSource ||
                spsLoading[selectedDoc?.document_id]
              }
            >
              <DeleteOutlined className="prompt-card-actions-head" />
            </Button>
          </Tooltip>
        </ConfirmModal>
      </Col>
    </Row>
  );
}

Header.propTypes = {
  promptDetails: PropTypes.object.isRequired,
  promptKey: PropTypes.text,
  setPromptKey: PropTypes.func.isRequired,
  progressMsg: PropTypes.object.isRequired,
  handleRun: PropTypes.func.isRequired,
  handleChange: PropTypes.func.isRequired,
  handleDelete: PropTypes.func.isRequired,
  updateStatus: PropTypes.object.isRequired,
  updatePlaceHolder: PropTypes.string,
  isCoverageLoading: PropTypes.bool.isRequired,
  isEditingTitle: PropTypes.bool.isRequired,
  setIsEditingTitle: PropTypes.func.isRequired,
  enableEdit: PropTypes.func.isRequired,
  expandCard: PropTypes.bool.isRequired,
  setExpandCard: PropTypes.func.isRequired,
  enabledProfiles: PropTypes.array.isRequired,
  spsLoading: PropTypes.object,
  handleSpsLoading: PropTypes.func.isRequired,
  handleGetOutput: PropTypes.func.isRequired,
};

export { Header };
