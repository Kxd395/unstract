import { Typography } from "antd";
import PropTypes from "prop-types";
import { displayPromptResult } from "../../../helpers/GetStaticData";
import { InfoCircleFilled } from "@ant-design/icons";

function DisplayPromptResult({ output }) {
  if (!output) {
    return (
      <Typography.Text className="prompt-not-ran">
        <span>
          <InfoCircleFilled style={{ color: "#F0AD4E" }} />
        </span>{" "}
        Yet to run
      </Typography.Text>
    );
  }

  return (
    <Typography.Paragraph className="prompt-card-display-output font-size-12">
      <div>{displayPromptResult(output, true)}</div>
    </Typography.Paragraph>
  );
}

DisplayPromptResult.propTypes = {
  output: PropTypes.any.isRequired,
};

export { DisplayPromptResult };
