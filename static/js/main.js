const scrollBtn = document.getElementById("scrollToTop");
scrollBtn.addEventListener("click", function (e) {
  e.preventDefault();
  window.scrollTo({ top: 0, behavior: "smooth" });
});