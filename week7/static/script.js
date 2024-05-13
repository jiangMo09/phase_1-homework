const handleMemberSubmit = () => {
  document.getElementById("loginForm").addEventListener("submit", (event) => {
    if (document.getElementById("terms").checked) {
      return;
    }

    alert("Please check the checkbox first");
    event.preventDefault();
  });
};

const handleSquareSubmit = (event) => {
  event.preventDefault();
  const positiveInteger = document.getElementById("positive-integer").value;

  if (isNaN(parseFloat(positiveInteger)) || parseFloat(positiveInteger) <= 0) {
    return alert("Please enter a positive number");
  }

  const actionUrl = "/square/" + positiveInteger;
  window.location.href = actionUrl;
};

const deleteMessage = async (message_id) => {
  const yes = confirm("你確定要刪除該留言嗎？");
  if (!yes) {
    return;
  }

  const formData = new FormData();
  formData.append("message_id", message_id);

  const response = await fetch("/deleteMessage", {
    method: "POST",
    body: formData
  });

  if (response.status == 200) {
    window.location.reload();
  }
};
