document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("textarea.markdown-editor").forEach((el) => {
    const easyMDE = new EasyMDE({
      element: el,
      spellChecker: false,
      autoDownloadFontAwesome: true,
      placeholder: "متن خود را اینجا بنویسید...",
      status: false,
      toolbar: [
        "bold","italic","heading","|","quote","unordered-list","ordered-list","|",
        "link","image","|","code","preview","fullscreen","|","guide",
      ],
      renderingConfig: {
        codeSyntaxHighlighting: true,
      },
    });
    easyMDE.codemirror.on("change", function () {
      document.querySelectorAll("pre code").forEach((block) => {
        hljs.highlightBlock(block);
      });
    });
  });
});
