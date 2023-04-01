
function s_odots(id){

    var element = document.getElementById('toggle-option'+id);
    element.classList.toggle('o-t-eneble');

}
function re_odots(id){

    var element = document.getElementById('toggle-option'+id);
    element.classList.toggle('o-t-eneble');

}

 // search student to add in hostel ajax


// update semester fee ajax

$(document).on('submit', '#update-semester-fee-form', function(e){
    e.preventDefault();

    var pk = $(this).attr('semester_student_id');

    req = $.ajax({
        type:'POST',
        url:'/semester-system/update-semester-fee/'+pk+'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
            student:pk
        }

    });
    var ele1 = document.getElementById('update-fee-input-semester');
    document.getElementById('content-loader-u-s-fee').classList.remove('d-none');
    ele1.classList.add('d-none');
    req.done(function(data){
        ele1.classList.remove('d-none');
        document.getElementById('content-loader-u-s-fee').classList.add('d-none');
        $('#student-detail').html(data);
    })


})





// search hostel students ajax

$(document).on('submit', '#search-semester-students', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/semester-system/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#create-post-body').html(data);
    })
})