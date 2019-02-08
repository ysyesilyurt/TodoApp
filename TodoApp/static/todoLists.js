$("#todolist-body").sortable();
$("#todolist-body").disableSelection();

countTodoLists();

//create new todoList
$('.add-todo-list').focus();
$('.add-todo-list').on('keypress',function (evnt) {
    // Stop form from submitting normally
    evnt.preventDefault;
    // Create item only if user pressed to 'enter'
    if (evnt.which == 13) {
        if($(this).val() != ''){
            var todo = $(this).val();
            createTodoList(todo);
        }
        else{
           // some validation
        }
    }
});

$('.table').on('click','.remove-item',function(){
    removeItem(this);
});

// count tasks
function countTodoLists(){
    var count = $("#todolist-body tr").length;
    $('.count-todolists').html(count);
}

//create task
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

//remove done task from list
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
