$("#todolist-body").sortable();
$("#todolist-body").disableSelection();

countTodoLists();

// create new TodoLists after entering the list name
$('.add-todo-list').focus();
$('.add-todo-list').on('keypress',function (evnt) {
    evnt.preventDefault;
    if (evnt.which == 13) {
        if($(this).val() != ''){
            var todo = $(this).val();
            createTodoList(todo);
        }
    }
});

// delete a TodoList
$('.table').on('click','.remove-item',function(){
    removeItem(this);
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
