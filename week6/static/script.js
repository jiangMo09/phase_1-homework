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

const getAPIMember = async () => {
  const usernameInput = document.getElementById("search-username");
  const searchResult = document.getElementById("search-result");

  const usernameValue = usernameInput.value;
  const response = await fetch(`/api/member?username=${usernameValue}`, {
    method: "GET"
  });

  const { data } = (await response.json()) || {};

  if (!data) {
    searchResult.innerHTML = "<p>查無此會員</p>";
    return;
  }

  const { name, username } = data;
  searchResult.innerHTML = `<p>${name} (${username})</p>`;
};

const patchAPIMemberName = async () => {
  const updateUsername = document.getElementById("update-username");
  const update = document.getElementById("update-result");
  const newUsername = updateUsername.value;

  const welcomeName = document.querySelector(".welcome-name");

  const response = await fetch(`/api/member`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name: newUsername })
  });

  const data = await response.json();

  if (data.error) {
    update.textContent = "更新失敗";
    return;
  }

  welcomeName.innerHTML = newUsername;
  update.textContent = "更新成功";
};
