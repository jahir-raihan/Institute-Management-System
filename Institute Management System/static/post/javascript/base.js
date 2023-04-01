// nav bar javascript



function myFunction() {
            
    var element = document.getElementById("toggle-nav");
    element.classList.toggle("disable");
}

function routineF(){

    var ele = document.getElementById('e-semesters');

    var eit = document.getElementById('result-i-t');
    eit.classList.remove('t-bg');

    ele.classList.toggle('r-disable');
}

function ebg(){
    var ele = document.getElementById('exam-i-t');
    ele.classList.toggle('t-bg')
}


// nav bar javascript end 


//container
function sideroutineF(){
    var ele = document.getElementById('side-e-semesters');
    var result = document.getElementById('side-r-semesters');
    var eit = document.getElementById('side-result-i-t');
    eit.classList.remove('side-bg');

    ele.classList.toggle('side-disable');
}



function sebg(){
    var ele = document.getElementById('side-exam-i-t');
    ele.classList.toggle('side-bg')
}


// container main

function odots(post_id){
    var dot = document.getElementById('toggle-option'+post_id);
    dot.classList.toggle('o-t-eneble')
    
}
function odots2(){
    var dot = document.getElementById('toggle-option');
    dot.classList.toggle('o-t-eneble')

}

function readMore(post_id){
    var readmore = document.getElementById('see-more'+post_id);
    
    readmore.classList.toggle('d-show');

    var rmb = document.getElementById('read-more-btn'+post_id);
    rmb.classList.toggle('d-none');

    var seeless = document.getElementById('see_less'+post_id);

    seeless.classList.add('d-show');

}

function readLess(post_id){


    var readmore = document.getElementById('see-more'+post_id);
    
    readmore.classList.remove('d-show');

    var rmb = document.getElementById('read-more-btn'+post_id);
    rmb.classList.remove('d-none');

    var seeless = document.getElementById('see_less'+post_id);

    seeless.classList.remove('d-show')
}

function show_notification(){
    var obj = document.getElementById('notification-toggle1');
    obj.classList.toggle('d-none');

}
function show_notification2(){
    var obj = document.getElementById('notification-toggle2');
    obj.classList.toggle('d-none');

}




// like button ajax

$(document).on('click', '.like-btn', function(e){


    e.preventDefault();
    var post_id = $(this).attr('post_id');
    req = $.ajax({
        url:'/',
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            like:post_id,
        }
    });
    req.done(function(data){
        $('#form-like-id'+post_id).html(data);
    });
});


 // search result ajax

 $(document).on('submit', '#search-result-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/college-system/search-result/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            roll:$('#roll').val(),
            registration:$('#registration').val(),
            semester:$('#id_semester').val()
        },
    });
    req.done(function(data){

        $('#s-r-body').html(data)

    })


 });

 // comment ajax

 $(document).on('submit', '.comment-form-home', function(e){
    e.preventDefault();

    var get_id = $(this).attr('comment_form');
    var comment_text = $('#write_comment'+get_id).val();

    req = $.ajax({
        url:'/',
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            post_id:get_id,

            comment:comment_text,
        }
    });
    req.done(function(data){

        $('#comment-body'+get_id).html(data);
    });

});

// view page comment ajax

$(document).on('submit', '.comment-form-view', function(e){
    e.preventDefault();

    var get_id = $(this).attr('comment_form');
    var comment_text = $('#write_comment'+get_id).val();

    req = $.ajax({
        url:'/',
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            post_id:get_id,
            page:'view',
            comment:comment_text,
        }
    });
    req.done(function(data){

        $('.comment-body').html(data);
    });

});


// search exam routine ajax
$(document).on('submit', '#search-exam-routine-form', function(e){
    e.preventDefault();
    req = $.ajax({
        url:'/college-system/view-routine/',
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            semester:$('#id_semester').val(),
            department:$('#id_department').val(),
        }
    });
    req.done(function(data){
        $('#search_exam_routine').html(data);
        
    });

});

// search class routine ajax

$(document).on('submit', '#search-class-routine-form', function(e){
    e.preventDefault();
    req = $.ajax({
        url:'/college-system/view-class-routine/',
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            semester:$('#id_semester').val(),
            department:$('#id_department').val(),
        }
    });
    req.done(function(data){

        $('#search-class-routine').html(data);
    });

});

// testing methods to not reload the page while submitting the data

// js for loader

function loader(text_id, loader_id, btn){
    ele = document.getElementById(text_id);
    button = document.getElementById(btn);
    button.disabled = 'true';
    button.classList.add('bg-gray');
    ele.style.display = 'none';
    ele1 = document.getElementById(loader_id);
    ele1.classList.remove('d-none');
}

// update subject mark ajax

$(document).on('submit', '#update-subject-mark-form', function(e){
    e.preventDefault();
    var get_id = $(this).attr('sub_id');
    req = $.ajax({
        url:'/dashboard/college-private-links/edit-subject-mark/'+ get_id + '/' ,
        type:'POST',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            mark:$('#mark').val(),
            tca:$('#t-c-a').val(),
            tfe:$('#t-f-e').val(),
            pca:$('#p-c-a').val(),
            pfe:$('#p-f-e').val(),

        }
    });
    document.getElementById('submit-text-e-sub-mark').classList.add('d-none');
    document.getElementById('content-loader-e-sub-mark').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-e-sub-mark').classList.add('d-none');
        $('#update-subject-mark').html(data);
    });

});

