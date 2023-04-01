
function h_odots(id){

    var element = document.getElementById('toggle-option'+id);
    element.classList.toggle('o-t-eneble');

}

 // search student to add in hostel ajax
$(document).on('submit', '#search-student-to-add-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/hostel/search_to_add/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#create-post-body').html(data);
    })
})

// update hostel fee ajax

$(document).on('submit', '#update-hostel-fee-form', function(e){
    e.preventDefault();
    console.log('submission got')
    var pk = $(this).attr('hostel_student_id');

    req = $.ajax({
        type:'POST',
        url:'/hostel/update-hotel-fee/'+pk+'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
            student:$('#student').val()
        }

    });
    var ele1 = document.getElementById('update-fee-input-hostel')
    ele1.classList.add('d-none');
    document.getElementById('content-loader-u-h-fee').classList.remove('d-none');
    req.done(function(data){
        ele1.classList.remove('d-none');
        document.getElementById('content-loader-u-h-fee').classList.add('d-none');
        $('#student-detail').html(data);
    })


})

// search hostel students ajax

$(document).on('submit', '#search-hostel-students', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/hostel/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#create-post-body').html(data);
    })
})