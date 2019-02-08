$("#not-done-items").sortable();
$("#not-done-items").disableSelection();
$("#done-items").sortable();
$("#done-items").disableSelection();

countTodos();
countDoneTodos();

// all done btn
$("#checkAll").click(function(){
    allDone("Mark all as Done");
});

// all undone btn
$("#uncheckAllDone").click(function(){
    allDone("Mark all as Undone");
});

// delete all btn
$("#deleteAll").click(function(){
    deleteAll("Delete all Undone");
});

// delete all undone btn
$("#deleteAllDone").click(function(){
    deleteAll("Delete all Done");
});

// create new TodoItems after entering the content
$('.add-todo').on('keypress',function (evnt) {
    // Stop form from submitting normally
    evnt.preventDefault;
    // Create item only if user pressed to 'enter'
    if (evnt.which == 13) {
        if($(this).val() != ''){
            var todo = $(this).val();
            createTodo(todo);
        }
    }
});

// mark task as done
$('.todolist').on('click','#not-done-items li input[type="checkbox"]',function(){
    if($(this).prop('checked')){
        var doneItem = $(this).parent().parent().find('label').text();
        $(this).parent().parent().parent().addClass('remove');
        done(doneItem);
        countTodos();
        countDoneTodos();
    }
});

//delete done task from "already done"
$('.todolist').on('click','.remove-item',function(){
    removeItem(this);
});

//undone task from "already done"
$('.todolist').on('click','.undone-item',function(){
    undoneItem(this);
});


// count done tasks
function countDoneTodos(){
    var count = $("#done-items li").length;
    $('.count-doneTodos').html(count);
}


// count tasks
function countTodos(){
    var count = $("#not-done-items li").length;
    $('.count-todos').html(count);
}

function createTodo(text){
    $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "Create",
             'itemContent': text},
			function (data) {
                if (data.result == "Fail")
                {
                    alert(data.appStatus);
                    // Clear prompt
                    $('.add-todo').val('');
                }
                else
                {
                    var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />'+ text +'</label>' +
                        '<span class="glyphicon glyphicon-align-justify" style="float: right;"></span></div></li>';
                    $('#not-done-items').append(markup);
                    // Clear prompt
                    $('.add-todo').val('');
                    countTodos();
                    countDoneTodos();
                }
			});
}

function done(doneItem){
    $.post(window.location.pathname,
        { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'submit': "Mark as Done",
            'itemContent': doneItem},
            function (data) {
				if (data.result == "Fail")
                    alert(data.appStatus);
				else
                {
                    var markup = '<li>'+ doneItem +'<button class="btn btn-default btn-xs pull-right  remove-item"><span class="glyphicon glyphicon-remove"></span></button>\n' +
                        '<button class="btn btn-default btn-xs pull-right  undone-item"><span class="glyphicon glyphicon-share-alt"></span></button></li>';
                    $('#done-items').append(markup);
                    $('.remove').remove();
                    countTodos();
                    countDoneTodos();
                }
			});
}

function allDone(allWhat){
    $.post(window.location.pathname,
        { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'submit': allWhat
        },
        function (data) {
            if (data.result == "Fail")
                    alert(data.appStatus);
            else
            {
                var currentItems = [];

                if (allWhat == "Mark all as Done")
                {
                    $('#not-done-items li').each(function () {
                        currentItems.push($(this).text());
                    });

                    // add to done
                    for (i = 0; i < currentItems.length; i++) {
                        $('#done-items').append('<li>' + currentItems[i] + '<button class="btn btn-default btn-xs pull-right  remove-item"><span class="glyphicon glyphicon-remove"></span></button>\n' +
                            '<button class="btn btn-default btn-xs pull-right  undone-item"><span class="glyphicon glyphicon-share-alt"></span></button></li>');
                    }

                    // currentItems
                    $('#not-done-items li').remove();
                    countTodos();
                    countDoneTodos();
                }
                else if (allWhat == "Mark all as Undone")
                {
                    $('#done-items li').each(function () {
                        currentItems.push($(this).text());
                    });

                    // add to done
                    for (i = 0; i < currentItems.length; i++) {
                        $('#not-done-items').append('<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />'+ currentItems[i] +'</label>' +
                            '<span class="glyphicon glyphicon-align-justify" style="float: right;"></span></div></li>');
                    }

                    // currentItems
                    $('#done-items li').remove();
                    countTodos();
                    countDoneTodos();
                }
            }
        }

        );
}

function deleteAll(deleteWhat){
    $.post(window.location.pathname,
        { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'submit': deleteWhat
        },
        function (data) {
            if (data.result == "Fail")
                    alert(data.appStatus);
            else
            {
                if (deleteWhat == "Delete all Undone")
                {
                    $('#not-done-items li').remove();
                    countTodos();
                    countDoneTodos();
                }
                else if (deleteWhat == "Delete all Done")
                {
                    $('#done-items li').remove();
                    countTodos();
                    countDoneTodos();
                }
            }
        }

        );
}

function removeItem(element){
    var removedItem = $(element).parent().text().replace(/\n/g, '');
    $.post(window.location.pathname,
            {   csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'submit': "Delete",
                'itemContent': removedItem},
                function (data) {
                    if (data.result == "Fail")
                        alert(data.appStatus);
                    else
                    {
                        $(element).parent().remove();
                        countTodos();
                        countDoneTodos();
                    }
            }
          );
}

function undoneItem(element){
    var undonedItem = $(element).parent().text().replace(/\n/g, '');
    $.post(window.location.pathname,
            {   csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'submit': "Undone",
                'itemContent': undonedItem},
                function (data) {
                    if (data.result == "Fail")
                        alert(data.appStatus);
                    else
                    {
                        var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />'+ undonedItem +'</label>' +
                            '<span class="glyphicon glyphicon-align-justify" style="float: right;"></span></div></li>';
                        $('#not-done-items').append(markup);
                        $(element).parent().remove();
                        countTodos();
                        countDoneTodos();
                    }
                }
          );
}
