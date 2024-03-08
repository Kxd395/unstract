import PropTypes from "prop-types";
import { useEffect, useRef, useState } from "react";
import "./DocumentParser.css";

import {
  promptStudioUpdateStatus,
  promptType,
} from "../../../helpers/GetStaticData";
import { useAxiosPrivate } from "../../../hooks/useAxiosPrivate";
import { useAlertStore } from "../../../store/alert-store";
import { useCustomToolStore } from "../../../store/custom-tool-store";
import { useSessionStore } from "../../../store/session-store";
import { EmptyState } from "../../widgets/empty-state/EmptyState";
import { NotesCard } from "../notes-card/NotesCard";
import { PromptCard } from "../prompt-card/PromptCard";
import { useExceptionHandler } from "../../../hooks/useExceptionHandler";

function DocumentParser({
  setOpenAddLlmModal,
  addPromptInstance,
  scrollToBottom,
  setScrollToBottom,
}) {
  const [updateStatus, setUpdateStatus] = useState({
    promptId: null,
    status: null,
  });
  const bottomRef = useRef(null);
  const { details, updateCustomTool } = useCustomToolStore();
  const { sessionDetails } = useSessionStore();
  const { setAlertDetails } = useAlertStore();
  const axiosPrivate = useAxiosPrivate();
  const handleException = useExceptionHandler();

  useEffect(() => {
    if (scrollToBottom) {
      // Scroll down to the lastest chat.
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
      setScrollToBottom(false);
    }
  }, [scrollToBottom]);

  const handleChange = async (
    event,
    promptId,
    dropdownItem,
    isUpdateStatus = false,
    isPromptUpdate = false
  ) => {
    const promptsAndNotes = details?.prompts || [];
    let name = "";
    let value = "";
    if (dropdownItem?.length) {
      name = dropdownItem;
      value = event;
    } else {
      name = event.target.name;
      value = event.target.value;
    }

    if (!value && name === "prompt_key") {
      // Return if the prompt or the prompt key is empty
      return;
    }

    const index = promptsAndNotes.findIndex(
      (item) => item?.prompt_id === promptId
    );

    if (index === -1) {
      setAlertDetails({
        type: "error",
        content: "Prompt not found",
      });
      return;
    }

    const promptDetails = promptsAndNotes[index];

    const body = {
      [`${name}`]: value,
    };
    const requestOptions = {
      method: "PATCH",
      url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/prompt/${promptDetails?.prompt_id}/`,
      headers: {
        "X-CSRFToken": sessionDetails?.csrfToken,
        "Content-Type": "application/json",
      },
      data: body,
    };

    handleUpdateStatus(
      isUpdateStatus,
      promptId,
      promptStudioUpdateStatus.isUpdating
    );

    return axiosPrivate(requestOptions)
      .then((res) => {
        const data = res?.data;
        const modifiedDetails = { ...details };
        const modifiedPrompts = [...(modifiedDetails?.prompts || [])].map(
          (item) => {
            if (item?.prompt_id === data?.prompt_id) {
              return data;
            }
            return item;
          }
        );
        modifiedDetails["prompts"] = modifiedPrompts;
        if (!isPromptUpdate) {
          updateCustomTool({ details: modifiedDetails });
        }
        handleUpdateStatus(
          isUpdateStatus,
          promptId,
          promptStudioUpdateStatus.done
        );
      })
      .catch((err) => {
        setAlertDetails(handleException(err, "Failed to update"));
        handleUpdateStatus(isUpdateStatus, promptId, null);
      })
      .finally(() => {
        if (isUpdateStatus) {
          setTimeout(() => {
            handleUpdateStatus(true, promptId, null);
          }, 3000);
        }
      });
  };

  const handleUpdateStatus = (isUpdate, promptId, value) => {
    if (!isUpdate) {
      return;
    }

    setUpdateStatus({
      promptId: promptId,
      status: value,
    });
  };

  const handleDelete = (promptId) => {
    const requestOptions = {
      method: "DELETE",
      url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/prompt/${promptId}/`,
      headers: {
        "X-CSRFToken": sessionDetails?.csrfToken,
      },
    };

    axiosPrivate(requestOptions)
      .then(() => {
        const modifiedDetails = { ...details };
        const modifiedPrompts = [...(modifiedDetails?.prompts || [])].filter(
          (item) => item?.prompt_id !== promptId
        );
        modifiedDetails["prompts"] = modifiedPrompts;
        updateCustomTool({ details: modifiedDetails });
        setAlertDetails({
          type: "success",
          content: "Deleted successfully",
        });
      })
      .catch((err) => {
        setAlertDetails(handleException(err, "Failed to delete"));
      });
  };

  if (!details?.prompts?.length) {
    return (
      <EmptyState
        text="Add prompt or a note and choose the LLM profile"
        btnText="Add Prompt"
        handleClick={() => addPromptInstance(promptType.prompt)}
      />
    );
  }

  return (
    <div className="doc-parser-layout">
      {details?.prompts.map((item) => {
        return (
          <div key={item.prompt_id}>
            <div className="doc-parser-pad-top" />
            {item.prompt_type === promptType.prompt && (
              <PromptCard
                promptDetails={item}
                handleChange={handleChange}
                handleDelete={handleDelete}
                setOpenAddLlmModal={setOpenAddLlmModal}
                updateStatus={updateStatus}
              />
            )}
            {item.prompt_type === promptType.notes && (
              <NotesCard
                details={item}
                handleChange={handleChange}
                handleDelete={handleDelete}
                updateStatus={updateStatus}
              />
            )}
            <div ref={bottomRef} className="doc-parser-pad-bottom" />
          </div>
        );
      })}
    </div>
  );
}

DocumentParser.propTypes = {
  setOpenAddLlmModal: PropTypes.func.isRequired,
  addPromptInstance: PropTypes.func.isRequired,
  scrollToBottom: PropTypes.bool.isRequired,
  setScrollToBottom: PropTypes.func.isRequired,
};

export { DocumentParser };
