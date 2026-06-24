document.addEventListener("DOMContentLoaded", function () {
  var tags = document.querySelector(".md-tags");
  var article = document.querySelector("article.md-content__inner");
  if (tags && article) {
    article.appendChild(tags);
  }
});
