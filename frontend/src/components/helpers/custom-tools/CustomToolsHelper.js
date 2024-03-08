import { useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";

import { useAxiosPrivate } from "../../../hooks/useAxiosPrivate";
import { useAlertStore } from "../../../store/alert-store";
import { useCustomToolStore } from "../../../store/custom-tool-store";
import { useSessionStore } from "../../../store/session-store";
import { SpinnerLoader } from "../../widgets/spinner-loader/SpinnerLoader";
import { SocketMessages } from "../socket-messages/SocketMessages";
import { useExceptionHandler } from "../../../hooks/useExceptionHandler";

function CustomToolsHelper() {
  const [isLoading, setIsLoading] = useState(true);
  const [logId, setLogId] = useState(null);
  const { id } = useParams();
  const { sessionDetails } = useSessionStore();
  const { updateCustomTool, setDefaultCustomTool } = useCustomToolStore();
  const { setAlertDetails } = useAlertStore();
  const navigate = useNavigate();
  const axiosPrivate = useAxiosPrivate();
  const handleException = useExceptionHandler();

  useEffect(() => {
    const updatedCusTool = {
      listOfDocs: [],
      details: {},
      defaultLlmProfile: "",
      llmProfiles: [],
      selectedDoc: null,
    };

    const reqOpsPromptStudio = {
      method: "GET",
      url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/${id}`,
    };

    setIsLoading(true);
    handleApiRequest(reqOpsPromptStudio)
      .then((res) => {
        const data = res?.data;
        updatedCusTool["defaultLlmProfile"] = data?.default_profile;
        updatedCusTool["details"] = data;
        updatedCusTool["selectedDoc"] = data?.output;
        setLogId(data?.log_id);

        const reqOpsDocs = {
          method: "GET",
          url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/file?tool_id=${data?.tool_id}`,
        };
        return handleApiRequest(reqOpsDocs);
      })
      .then((res) => {
        const data = (res?.data || [])
          ?.filter(
            (item) => item?.name !== "extract" && item?.name !== "summarize"
          )
          ?.map((item) => item?.name);
        updatedCusTool["listOfDocs"] = data;

        const reqOpsDropdownItems = {
          method: "GET",
          url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/select_choices`,
        };
        return handleApiRequest(reqOpsDropdownItems);
      })
      .then((res) => {
        const data = res?.data;
        updatedCusTool["dropdownItems"] = data;

        const reqOpsLlmProfiles = {
          method: "GET",
          url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/profile-manager/`,
        };

        return handleApiRequest(reqOpsLlmProfiles);
      })
      .then((res) => {
        const data = res?.data;
        updatedCusTool["llmProfiles"] = data;
      })
      .catch((err) => {
        setAlertDetails(handleException(err, "Failed to load the custom tool"));
        navigate(`/${sessionDetails?.orgName}/tools`);
      })
      .finally(() => {
        updateCustomTool(updatedCusTool);
        setIsLoading(false);
      });
  }, [id]);

  useEffect(() => {
    return () => {
      setDefaultCustomTool();
    };
  }, []);

  const handleApiRequest = async (requestOptions) => {
    return axiosPrivate(requestOptions)
      .then((res) => res)
      .catch((err) => {
        throw err;
      });
  };

  if (isLoading) {
    return <SpinnerLoader />;
  }
  return (
    <>
      <Outlet />
      <SocketMessages logId={logId} />
    </>
  );
}

export { CustomToolsHelper };
