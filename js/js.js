var form = document.querySelector("#form")

form.addEventListener("submit", function(e) {
    e.preventDefault();
    const XHR = new XMLHttpRequest();
    const data = new FormData(form);
    for (const [name, value] of Object.entries(data)) {
        FD.append(name, value);
      }
    
      // Define what happens on successful data submission
      XHR.addEventListener("load", (event) => {
        alert("Данные отправлены!.");
      });
    
      // Define what happens in case of an error
      XHR.addEventListener("error", (event) => {
        alert("Упс! Что-то пошло не так.");
      });
    
      // Set up our request
      XHR.open("GET", "/");
    
      // Send our FormData object; HTTP headers are set automatically
      XHR.send(FD);
  })