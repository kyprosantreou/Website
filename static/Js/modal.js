var modal = document.getElementById("taskModal");
var btn = document.getElementById("openModalBtn");
var span = document.getElementsByClassName("close")[0];
var titleInput = document.getElementById("taskTitle");
var contentInput = document.getElementById("taskContent");

btn.onclick = function() {
    modal.style.display = "block";
    titleInput.value = "";
    contentInput.value = "";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById("taskForm").addEventListener("submit", function(event) {
    event.preventDefault(); 
    var title = titleInput.value;
    var content = contentInput.value;
    console.log("Title:", title, "Content:", content); 

    var task = document.createElement("div");
    task.classList.add("task");
    task.innerHTML = "<h3>" + title + "</h3><p>" + content + "</p>";

    var editBtn = document.createElement("button");
    editBtn.textContent = "Edit Task";
    editBtn.classList.add("edit-btn");
    editBtn.onclick = function() {
        openEditModal(task, title, content);
    };
    task.appendChild(editBtn); 

    var deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete Task";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = function() {
        task.remove(); 
    };
    task.appendChild(deleteBtn); 

    var todoColumn = document.getElementById("todo");
    todoColumn.appendChild(task);

    modal.style.display = "none"; 
});

function openEditModal(task, title, content) {
    var editModal = document.getElementById("editModal");
    var editTitleInput = document.getElementById("editTaskTitle");
    var editContentInput = document.getElementById("editTaskContent");

    editModal.task = task;

    editTitleInput.value = title;
    editContentInput.value = content;

    editModal.style.display = "block";
}

document.getElementById("editTaskForm").addEventListener("submit", function(event) {
    event.preventDefault(); 

    var task = document.getElementById("editModal").task;
    var title = document.getElementById("editTaskTitle").value;
    var content = document.getElementById("editTaskContent").value;

    task.querySelector("h3").textContent = title;
    task.querySelector("p").textContent = content;

    document.getElementById("editModal").style.display = "none";
});

document.getElementById("editCloseBtn").addEventListener("click", function() {
    document.getElementById("editModal").style.display = "none";
});

