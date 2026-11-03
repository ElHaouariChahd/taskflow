const API = "/api/tasks";
let currentFilter = "all";

const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const priority = document.getElementById("task-priority");
const list = document.getElementById("task-list");
const counter = document.getElementById("counter");
const errorBox = document.getElementById("error");
const filterButtons = document.querySelectorAll(".filter");

// Appel générique à l'API, avec gestion des erreurs HTTP
async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`Erreur serveur (${res.status})`);
  return res.status === 204 ? null : res.json();
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = !message;
}

async function refresh() {
  try {
    const [tasks, active] = await Promise.all([
      request(`${API}?status=${currentFilter}`),
      request(`${API}?status=active`),
    ]);
    render(tasks);
    const n = active.length;
    counter.textContent = `${n} tâche${n > 1 ? "s" : ""} restante${
      n > 1 ? "s" : ""
    }`;
    showError("");
  } catch (err) {
    showError(err.message);
  }
}

function render(tasks) {
  list.innerHTML = "";
  tasks.forEach((t) => {
    const li = document.createElement("li");
    li.className = `task ${t.priority}${t.done ? " done" : ""}`;
    li.dataset.id = t.id;
    li.innerHTML = `<input type="checkbox" ${t.done ? "checked" : ""}>
      <span></span>
      <button class="delete" title="Supprimer">✕</button>`;
    li.querySelector("span").textContent = t.title;
    list.appendChild(li);
  });
}

refresh();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await request(API, {
      method: "POST",
      body: JSON.stringify({ title: input.value, priority: priority.value }),
    });
    input.value = "";
    refresh();
  } catch (err) {
    showError(err.message);
  }
});

list.addEventListener("click", async (e) => {
  const li = e.target.closest("li");
  if (!li) return;
  const url = `${API}/${li.dataset.id}`;
  try {
    if (e.target.classList.contains("delete")) {
      await request(url, { method: "DELETE" });
    } else if (e.target.type === "checkbox") {
      await request(url, {
        method: "PATCH",
        body: JSON.stringify({ done: e.target.checked }),
      });
    } else {
      return;
    }
    refresh();
  } catch (err) {
    showError(err.message);
  }
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    filterButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    refresh();
  });
});
