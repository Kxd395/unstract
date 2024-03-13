import { Input, Space, Typography } from "antd";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import "./PreAndPostAmbleModal.css";

import { useAlertStore } from "../../../store/alert-store";
import { useCustomToolStore } from "../../../store/custom-tool-store";
import { CustomButton } from "../../widgets/custom-button/CustomButton";
import { useExceptionHandler } from "../../../hooks/useExceptionHandler";

const fieldNames = {
  preamble: "PREAMBLE",
  postamble: "POSTAMBLE",
};

function PreAndPostAmbleModal({ type, handleUpdateTool }) {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const { details, updateCustomTool } = useCustomToolStore();
  const { setAlertDetails } = useAlertStore();
  const handleException = useExceptionHandler();

  useEffect(() => {
    if (type === fieldNames.preamble) {
      setTitle("Preamble");
      setText(details?.preamble || "");
      return;
    }

    if (type === fieldNames.postamble) {
      setTitle("Postamble");
      setText(details?.postamble || "");
    }
  }, [type]);

  const handleSave = () => {
    const body = {};
    if (type === fieldNames.preamble) {
      body["preamble"] = text;
    }

    if (type === fieldNames.postamble) {
      body["postamble"] = text;
    }
    handleUpdateTool(body)
      .then((res) => {
        const data = res?.data;
        const updatedData = {
          preamble: data?.preamble || "",
          postamble: data?.postamble || "",
        };
        const updatedDetails = { ...details, ...updatedData };
        updateCustomTool({ details: updatedDetails });
        setAlertDetails({
          type: "success",
          content: "Saved successfully",
        });
      })
      .catch((err) => {
        setAlertDetails(handleException(err, "Failed to update."));
      });
  };

  return (
    <>
      <div className="pre-post-amble-body">
        <Space direction="vertical" className="pre-post-amble-body-space">
          <div>
            <Typography.Text strong className="pre-post-amble-title">
              {title}
            </Typography.Text>
          </div>
          <div>
            <div>
              <Typography.Text>Add {title}</Typography.Text>
            </div>
          </div>
          <div>
            <Input.TextArea
              rows={3}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
          </div>
        </Space>
      </div>
      <div className="display-flex-right">
        <Space>
          <CustomButton type="primary" onClick={handleSave}>
            Save
          </CustomButton>
        </Space>
      </div>
    </>
  );
}

PreAndPostAmbleModal.propTypes = {
  type: PropTypes.string.isRequired,
  handleUpdateTool: PropTypes.func.isRequired,
};

export { PreAndPostAmbleModal };
