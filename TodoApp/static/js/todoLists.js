$("#todolist-body").sortable({
        update: function(event, data) {
            var listName = data.item.find("td:first").text();
            var todoLists = [];
            var newIndex;

            $('#todolist-body tr').each(function () {
                todoLists.push($(this).context.children[0].innerText);
            });

            for (i = 0; i < todoLists.length; i++) {
                if (todoLists[i] == listName) {
                    newIndex = i;
                    break;
                }
            }

            $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "listSort",
             'listName': listName,
             'newIndex': newIndex},
			function (data) {
                if (data.result == "Fail")
                    alert(data.appStatus);
			});
        }
});
$("#todolist-body").disableSelection();



countTodoLists();

// create new TodoLists after entering the list name
$('.add-todo-list').focus();
$('.add-todo-list').on('keypress',function (event) {
    event.preventDefault;
    if (event.which == 13) {
        if($(this).val() != ''){
            var todo = $(this).val();
            createTodoList(todo);
        }
    }
});

// delete a TodoList
$('#todolist-body').on('click','.remove-item',function(){
    removeItem(this);
});

// edit name of a TodoList
$('#todolist-body').on('click','.edit-item',function(){
    editItem(this);
});

// count TodoLists
function countTodoLists(){
    var count = $("#todolist-body tr").length;
    $('.count-todolists').html(count);
}

function createTodoList(text){
    $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "Create",
             'listName': text},
			function (data) {
                if (data.result == "Fail")
                {
                    alert(data.appStatus);
                }
                else
                {
                    location.reload();
                    // Clear prompt
                    $('.add-todo').val('');
                    countTodoLists();
                }
			});
}

function removeItem(element){
    var removedItem = $(element).parent().parent().find("td:first").text();
    $.post(window.location.pathname,
            {   csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'submit': "Delete",
                'listName': removedItem},
                function (data) {
                    if (data.result == "Fail")
                        alert(data.appStatus);
                    else
                    {
                        $(element).parent().parent().remove();
                        countTodoLists();
                    }
            }
          );
}

function editItem(element){
    var editedItem = $(element).parent().parent().find("td:first").text();
    var newItem = prompt("Please enter new list name:", editedItem);

    while (newItem == "")
    {
        alert("Please choose a valid TodoList name");
        newItem = prompt("Please enter new list name:", editedItem);
    }

    if (newItem == null)
        return;

    $.post(window.location.pathname,
            {   csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'submit': "Edit",
                'listName': editedItem,
                'newName': newItem},
                function (data) {
                    if (data.result == "Fail")
                        alert(data.appStatus);
                    else
                        location.reload();
                }
          );
}