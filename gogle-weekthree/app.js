// app.js – Handles UI, Supabase CRUD, and Gemini difficulty classification
import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/esm/index.js";
import { SUPABASE_URL, SUPABASE_ANON_KEY, classifyDifficulty } from "./config.js";

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// DOM elements
const taskInput = document.getElementById("new-task");
const addBtn = document.getElementById("add-btn");
const taskList = document.getElementById("task-list");

// Load existing tasks on startup
async function loadTasks() {
  const { data, error } = await supabase.from("tasks").select("*" ).order("created_at", { ascending: false });
  if (error) {
    console.error("Error loading tasks:", error);
    return;
  }
  taskList.innerHTML = "";
  data.forEach(renderTask);
}

// Render a single task item
function renderTask(task) {
  const item = document.createElement("div");
  item.className = "task-item";
  item.dataset.id = task.id;

  const contentDiv = document.createElement("div");
  contentDiv.className = "task-content";
  contentDiv.textContent = task.content;

  const badge = document.createElement("span");
  badge.className = `difficulty-badge difficulty-${task.difficulty.toLowerCase()}`;
  badge.textContent = task.difficulty;

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "task-actions";

  const editBtn = document.createElement("button");
  editBtn.textContent = "✏️";
  editBtn.title = "Edit";
  editBtn.onclick = () => editTask(task.id, task.content);

  const delBtn = document.createElement("button");
  delBtn.textContent = "🗑️";
  delBtn.title = "Delete";
  delBtn.onclick = () => deleteTask(task.id);

  actionsDiv.append(editBtn, delBtn);
  item.append(badge, contentDiv, actionsDiv);
  taskList.appendChild(item);
}

// Add a new task
async function addTask() {
  const text = taskInput.value.trim();
  if (!text) return;
  addBtn.disabled = true;
  const difficulty = await classifyDifficulty(text);
  const { data, error } = await supabase.from("tasks").insert({ content: text, difficulty });
  if (error) {
    console.error("Insert error:", error);
  } else {
    renderTask(data[0]);
    taskInput.value = "";
  }
  addBtn.disabled = false;
}

// Edit existing task (simple prompt for demo)
async function editTask(id, oldContent) {
  const newContent = prompt("Edit task", oldContent);
  if (newContent === null) return; // cancel
  const trimmed = newContent.trim();
  if (!trimmed) return;
  const difficulty = await classifyDifficulty(trimmed);
  const { error } = await supabase.from("tasks").update({ content: trimmed, difficulty }).eq("id", id);
  if (error) {
    console.error("Update error:", error);
    return;
  }
  // Update UI
  const item = document.querySelector(`.task-item[data-id='${id}']`);
  if (item) {
    item.querySelector('.task-content').textContent = trimmed;
    const badge = item.querySelector('.difficulty-badge');
    badge.textContent = difficulty;
    badge.className = `difficulty-badge difficulty-${difficulty.toLowerCase()}`;
  }
}

// Delete task
async function deleteTask(id) {
  const { error } = await supabase.from("tasks").delete().eq("id", id);
  if (error) {
    console.error("Delete error:", error);
    return;
  }
  const item = document.querySelector(`.task-item[data-id='${id}']`);
  if (item) item.remove();
}

// Event listeners
addBtn.addEventListener("click", addTask);
taskInput.addEventListener("keypress", e => { if (e.key === "Enter") addTask(); });

// Initial load
loadTasks();
