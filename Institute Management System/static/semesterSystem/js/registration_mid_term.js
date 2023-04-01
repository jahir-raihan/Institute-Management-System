$(document).on('submit', '#update-registration-fee-form', function(e){

    e.preventDefault();

    var pk = $(this).attr('registration_student_id');

    req = $.ajax({
        type:'POST',
        url:'/semester-system/registration/update-registration-fee/'+pk+'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
            student:$('#student').val()
        }

    });
    var ele1 = document.getElementById('update-fee-input-registration');
    document.getElementById('content-loader-u-r-fee').classList.remove('d-none');
    ele1.classList.add('d-none');
    req.done(function(data){
        ele1.classList.remove('d-none');
        document.getElementById('content-loader-u-r-fee').classList.add('d-none');
        $('#student-detail-registration').html(data);
    })


})

// search registration fee form ajax


$(document).on('submit', '#search-registration-students', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/semester-system/registration/registration-home/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#create-post-body').html(data);
    })
})


// ajax for mid term system

$(document).on('submit', '#update-midterm-fee-form', function(e){

    e.preventDefault();

    var pk = $(this).attr('midterm_student_id');

    req = $.ajax({
        type:'POST',
        url:'/semester-system/midterm/update-midterm-fee/'+pk+'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
            student:$('#student').val()
        }

    });
    var ele1 = document.getElementById('update-fee-input-midterm');
    document.getElementById('content-loader-u-m-t-fee').classList.remove('d-none');
    ele1.classList.add('d-none');
    req.done(function(data){
        ele1.classList.remove('d-none');
        document.getElementById('content-loader-u-m-t-fee').classList.add('d-none');
        $('#student-detail-midterm').html(data);
    })


})

// search midterm fee form ajax


$(document).on('submit', '#search-midterm-students', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/semester-system/midterm/midterm-home/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#create-post-body').html(data);
    })
})

