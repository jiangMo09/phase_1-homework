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
