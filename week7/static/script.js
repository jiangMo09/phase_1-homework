const handleMemberSubmit = () => {
  document.getElementById("loginForm").addEventListener("submit", (event) => {
    if (document.getElementById("terms").checked) {
      return;
    }

    alert("Please check the checkbox first");
    event.preventDefault();
  });
};

const getAPIMember = async () => {
  const usernameInput = document.getElementById("search-username");
  const searchResult = document.getElementById("search-result");

  const usernameValue = usernameInput.value;
  const response = await fetch(`/api/member?username=${usernameValue}`, {
    method: "GET"
  });

  const { data } = (await response.json()) || {};
  const { name, username } = data || {};

  if (!username) {
    searchResult.innerHTML = "<p>查無此會員</p>";
  }

  searchResult.innerHTML = `<p>${name} (${username})</p>`;
};
