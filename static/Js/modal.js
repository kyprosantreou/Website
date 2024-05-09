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

// Function to add "Move to In Progress" button to a task
function addMoveToInProgressButton(task) {
    var button = document.createElement("button");
    button.textContent = "Mark as In Progress";
    button.classList.add("move-to-in-progress-btn");
    button.onclick = function() {
        moveTaskToInProgress(task);
    };
    task.appendChild(button);
}

// Function to move the task from "todo" to "in progress" column
function moveTaskToInProgress(task) {
    var inProgressColumn = document.getElementById("inProgress");
    task.querySelector(".move-to-in-progress-btn").remove(); // Remove the button
    inProgressColumn.appendChild(task); // Append the task to the "in progress" column
}

// Function to add "Move to Done" button to a task
function addMoveToDoneButton(task) {
    var button = document.createElement("button");
    button.textContent = "Mark as Done"; // Changed the button text
    button.classList.add("move-to-done-btn");
    button.onclick = function() {
        moveTaskToDone(task);
    };
    task.appendChild(button);
}

// Function to move the task from "in progress" to "done" column
function moveTaskToDone(task) {
    var doneColumn = document.getElementById("done"); // Changed the variable name to 'doneColumn'
    task.querySelector(".move-to-done-btn").remove(); // Remove the button
    doneColumn.appendChild(task); // Append the task to the "done" column
}

// Function to add the date and time of creation to a task
function addCreationDateTime(task) {
    var dateTime = new Date().toLocaleString(); // Get current date and time
    var span = document.createElement("span");
    span.textContent = "Created: " + dateTime;
    span.classList.add("task-date");
    task.appendChild(span);
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
        openEditModal(task, task.querySelector("h3").textContent, task.querySelector("p").textContent);
    };
    task.appendChild(editBtn); 

    var deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete Task";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = function() {
        task.remove(); 
    };
    task.appendChild(deleteBtn); 

    // Add "Move to In Progress" button
    addMoveToInProgressButton(task);
    // Add "Move to Done" button
    addMoveToDoneButton(task);
    // Add creation date and time
    addCreationDateTime(task);

    var todoColumn = document.getElementById("todo");
    todoColumn.appendChild(task);

    modal.style.display = "none"; 
});

// Function to open the edit modal
function openEditModal(task, title, content) {
    var editModal = document.getElementById("editModal");
    var editTitleInput = document.getElementById("editTaskTitle");
    var editContentInput = document.getElementById("editTaskContent");

    // Store task reference
    editModal.task = task;

    // Store original content
    editModal.originalTitle = title;
    editModal.originalContent = content;

    // Use the previously edited content if available
    if (editModal.editedTitle && editModal.editedContent) {
        editTitleInput.value = editModal.editedTitle;
        editContentInput.value = editModal.editedContent;
    } else {
        editTitleInput.value = title;
        editContentInput.value = content;
    }

    editModal.style.display = "block";
}

// Function to add move to in progress functionality to the edit modal
document.getElementById("editModal").addEventListener("click", function(event) {
    if (event.target && event.target.classList.contains("move-to-in-progress-btn")) {
        var task = event.target.parentNode;
        moveTaskToInProgress(task);
    }
});

// Function to handle the submission of the edit task form
document.getElementById("editTaskForm").addEventListener("submit", function(event) {
    event.preventDefault(); 

    var editModal = document.getElementById("editModal");
    var task = editModal.task;
    var titleInput = document.getElementById("editTaskTitle");
    var contentInput = document.getElementById("editTaskContent");
    var title = titleInput.value;
    var content = contentInput.value;

    // Update original content in edit modal
    editModal.originalTitle = title;
    editModal.originalContent = content;

    // Store edited content
    editModal.editedTitle = title;
    editModal.editedContent = content;

    task.querySelector("h3").textContent = title;
    task.querySelector("p").textContent = content;

    editModal.style.display = "none";
});

// Function to handle closing the edit modal
document.getElementById("editCloseBtn").addEventListener("click", function() {
    var editModal = document.getElementById("editModal");

    // Clear edited content when closing the modal
    editModal.editedTitle = null;
    editModal.editedContent = null;

    editModal.style.display = "none";
});
