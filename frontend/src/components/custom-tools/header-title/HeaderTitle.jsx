import { ArrowLeftOutlined, EditOutlined } from "@ant-design/icons";
import { Button, Typography } from "antd";
import "./HeaderTitle.css";
import { useNavigate } from "react-router-dom";
import { useCustomToolStore } from "../../../store/custom-tool-store";

function HeaderTitle({}) {
  const navigate = useNavigate();
  const { details } = useCustomToolStore();

  return (
    <div className="custom-tools-header">
      <div>
        <Button
          size="small"
          type="text"
          onClick={() => navigate(`/${sessionDetails?.orgName}/tools`)}
        >
          <ArrowLeftOutlined />
        </Button>
      </div>
      <div className="custom-tools-name">
        <Typography.Text strong>{details?.tool_name}</Typography.Text>
        <Button size="small" type="text" disabled>
          <EditOutlined />
        </Button>
      </div>
    </div>
  );
}
export { HeaderTitle };
