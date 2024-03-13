import { Checkbox, Form, Input, Select, Space, Switch, Typography } from "antd";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";

import { useCustomToolStore } from "../../../store/custom-tool-store";
import { useAlertStore } from "../../../store/alert-store";
import { CustomButton } from "../../widgets/custom-button/CustomButton";
import { useExceptionHandler } from "../../../hooks/useExceptionHandler";

const fieldNames = {
  SUMMARIZE_LLM_PROFILE: "summarize_llm_profile",
  SUMMARIZE_PROMPT: "summarize_prompt",
  SUMMARIZE_CONTEXT: "summarize_context",
  SUMMARIZE_AS_SOURCE: "summarize_as_source",
};
function SelectLlmProfileModal({ llmItems, handleUpdateTool }) {
  const [selectedLlm, setSelectedLlm] = useState("");
  const [prompt, setPrompt] = useState("");
  const [isContext, setIsContext] = useState(false);
  const [isSource, setIsSource] = useState(false);
  const [isModified, setIsModified] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { details, updateCustomTool } = useCustomToolStore();
  const { setAlertDetails } = useAlertStore();
  const handleException = useExceptionHandler();

  useEffect(() => {
    setPrompt(details?.summarize_prompt);
    setIsContext(details?.summarize_context);
    setIsSource(details?.summarize_as_source);
  }, []);

  useEffect(() => {
    if (llmItems?.length) {
      setSelectedLlm(details?.summarize_llm_profile);
    }
  }, [llmItems]);

  const handleStateUpdate = (fieldName, value) => {
    if (fieldName === fieldNames.SUMMARIZE_LLM_PROFILE) {
      setSelectedLlm(value);
    }

    if (fieldName === fieldNames.SUMMARIZE_PROMPT) {
      setPrompt(value);
    }

    if (fieldName === fieldNames.SUMMARIZE_CONTEXT) {
      setIsContext(value);
      setIsSource(value ? isSource : false);
    }

    if (fieldName === fieldNames.SUMMARIZE_AS_SOURCE) {
      setIsSource(value);
    }

    if (!isModified) {
      setIsModified(true);
    }
  };

  const handleSave = () => {
    const body = {
      [fieldNames.SUMMARIZE_LLM_PROFILE]: selectedLlm,
      [fieldNames.SUMMARIZE_PROMPT]: prompt,
      [fieldNames.SUMMARIZE_CONTEXT]: isContext,
      [fieldNames.SUMMARIZE_AS_SOURCE]: isSource,
    };

    setIsLoading(true);
    handleUpdateTool(body)
      .then(() => {
        const updatedDetails = { ...details };
        updatedDetails["summarize_llm_profile"] = selectedLlm;
        updatedDetails["summarize_prompt"] = prompt;
        updatedDetails["summarize_context"] = isContext;
        updatedDetails["summarize_as_source"] = isSource;
        updateCustomTool({ details: updatedDetails });

        setAlertDetails({
          type: "success",
          content: "Successfully updated the LLM profile",
        });
        setIsModified(false);
      })
      .catch((err) => {
        setAlertDetails(
          handleException(err, "Failed to update the LLM profile")
        );
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div>
      <div className="select-llm-pro-header">
        <Typography.Text strong className="pre-post-amble-title">
          Summarize Manager
        </Typography.Text>
      </div>
      <Form layout="vertical">
        <div className="pre-post-amble-body">
          <Form.Item label="Select LLM Profile">
            <Select
              placeholder="Select Eval LLM"
              value={selectedLlm}
              options={llmItems}
              onChange={(value) =>
                handleStateUpdate(fieldNames.SUMMARIZE_LLM_PROFILE, value)
              }
            />
          </Form.Item>
          <Form.Item label="Prompt">
            <Input.TextArea
              rows={3}
              placeholder="Enter Prompt"
              name={fieldNames.SUMMARIZE_PROMPT}
              value={prompt}
              onChange={(e) => handleStateUpdate(e.target.name, e.target.value)}
            />
          </Form.Item>
          <Form.Item>
            <Space>
              <Switch
                value={isContext}
                disabled={!selectedLlm}
                size="small"
                onChange={(value) =>
                  handleStateUpdate(fieldNames.SUMMARIZE_CONTEXT, value)
                }
              />
              <Typography.Text>Summarize Context</Typography.Text>
            </Space>
          </Form.Item>
          <Form.Item>
            <Space>
              <Checkbox
                checked={isSource}
                disabled={!isContext || !selectedLlm}
                size="small"
                onChange={(e) =>
                  handleStateUpdate(
                    fieldNames.SUMMARIZE_AS_SOURCE,
                    e.target.checked
                  )
                }
              />
              <Typography.Text>Use summarize context as source</Typography.Text>
            </Space>
          </Form.Item>
        </div>
        <div className="display-flex-right">
          <CustomButton
            type="primary"
            onClick={handleSave}
            disabled={!isModified}
            loading={isLoading}
          >
            Save
          </CustomButton>
        </div>
      </Form>
    </div>
  );
}

SelectLlmProfileModal.propTypes = {
  llmItems: PropTypes.array.isRequired,
  handleUpdateTool: PropTypes.func.isRequired,
};

export { SelectLlmProfileModal };
