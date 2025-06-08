const toggleBtn = document.getElementById("search-toggle");
const searchForm = document.getElementById("search-form");

let open = false;

toggleBtn.addEventListener("click", () => {
  open = !open;
  if (open) {
    searchForm.classList.remove("translate-x-full", "opacity-0", "pointer-events-none");
    searchForm.classList.add("translate-x-0", "opacity-100");
  } else {
    searchForm.classList.add("translate-x-full", "opacity-0", "pointer-events-none");
    searchForm.classList.remove("translate-x-0", "opacity-100");
  }
});

document.addEventListener("click", (e) => {
  if (!searchForm.contains(e.target) && !toggleBtn.contains(e.target)) {
    searchForm.classList.add("translate-x-full", "opacity-0", "pointer-events-none");
    searchForm.classList.remove("translate-x-0", "opacity-100");
    open = false;
  }
});
