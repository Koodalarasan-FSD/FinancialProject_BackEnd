



/* Hiding & Unhiding Password */


let passIcon = document.querySelectorAll(".eye-icon");

passIcon.forEach((icon) => {
  icon.addEventListener("click", () => {
    let passwordInputs = icon.parentElement.querySelectorAll(".password");

    passwordInputs.forEach((input) => {
      //if the input type is password, making it to text
      //and changin icon
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye-slash", "fa-eye");
        return;
      }

      else
      {
      input.type = "password";
      icon.classList.replace("fa-eye", "fa-eye-slash");

    }
      });
  });
});


