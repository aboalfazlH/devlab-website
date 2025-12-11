document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".quill-editor").forEach((textarea) => {
    textarea.style.display = "none";
    const wrapper = document.createElement("div");
    wrapper.classList.add("quill-wrapper");
    const container = document.createElement("div");
    container.style.minHeight = "250px";
    container.style.marginBottom = "20px";
    textarea.parentNode.insertBefore(wrapper, textarea);
    wrapper.appendChild(container);
    const quill = new Quill(container, {
      theme: "snow",
      modules: {
        toolbar: {
          container: [
            [{ header: [1, 2, 3, 4, 5, false] }],
            [{ font: [] }],
            [{ size: ["small", false, "large", "huge"] }],
            ["bold", "italic", "underline", "strike"],
            [{ color: [] }, { background: [] }],
            [{ script: "sub" }, { script: "super" }],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ align: [] }],
            ["blockquote", "code-block"],
            ["link", "image", "video"],
            ["clean"],
          ],
        },
      },
    });
    quill.root.innerHTML = textarea.value;
    quill.on("text-change", () => {
      textarea.value = quill.root.innerHTML;
    });
  });
});
