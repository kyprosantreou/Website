function addTask() {
    var taskInput = document.getElementById("taskInput");
    var taskText = taskInput.value.trim();
    if (taskText !== "") {
      var task = document.createElement("div");
      task.className = "task";
      task.textContent = taskText;
      taskInput.value = "";
      document.getElementById("todo").appendChild(task);
    }
  }
  