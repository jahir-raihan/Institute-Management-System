function off2(){

    document.getElementById('overlay3').style.display = "none";
}

// authenticate admin ajax
$(document).on('submit', '#admin-authenticate-form' , function(e){
    e.preventDefault();
        req = $.ajax({
            url: '/restricted-url/authenticate-admin-password/',
            type: 'POST',
            data: {
                password:$('#authenticate-password').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                email:$('#r-email').val()
            }


    });

    req.done(function(data){
        $('#overlay-body-r-t').html(data);
    })
})

// authenticate admin for semester system ajax
$(document).on('submit', '#u-semester-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/dashboard/authenticate-admin/',
        type: 'POST',
        data: {
            password:$('#s-u-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#s-u-auth-email').val()
        }



    });
    document.getElementById('submit-text-u-semester-r').classList.add('d-none');
    document.getElementById('content-loader-u-s-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-s-r').classList.add('d-none');

        $('#overlay-body-u-semester').html(data);
    })
})

// authenticate admin for uploading deafen student list

$(document).on('submit', '#deafen-list-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/restricted-url/authenticate-admin-for-deafen-list/',
        type: 'POST',
        data: {
            password:$('#d-l-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#d-l-auth-email').val()
        }



    });
    document.getElementById('submit-text-deafen-list').classList.add('d-none');
    document.getElementById('content-loader-d-l').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-d-l').classList.add('d-none');

        $('#overlay-body-deafen-list').html(data);
    })
})
// authenticate admin for uploading student list ajax

$(document).on('submit', '#student-list-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/restricted-url/authenticate-admin-for-student-list/',
        type: 'POST',
        data: {
            password:$('#s-l-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#s-l-auth-email').val()
        }



    });
    document.getElementById('submit-text-student-list').classList.add('d-none');
    document.getElementById('content-loader-s-l').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-s-l').classList.add('d-none');

        $('#overlay-body-student-list').html(data);
    })
})

// authenticate hostel manage or admin to update hostel data
$(document).on('submit', '#u-hostel-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/dashboard/authenticate-admin-to-update-hostel-data/',
        type: 'POST',
        data: {
            password:$('#h-u-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#h-u-auth-email').val()
        }



    });
    document.getElementById('submit-text-u-hostel-r').classList.add('d-none');
    document.getElementById('content-loader-u-h-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-h-r').classList.add('d-none');

        $('#overlay-body-u-hostel-data').html(data);
    })
})


// update semester data ajax

$(document).on('submit', '#u-semester-form-ajax' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/dashboard/authenticate-admin/update-semester/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

        }



    });
    document.getElementById('submit-text-u-semester-submit-r').classList.add('d-none');
    document.getElementById('content-loader-u-s-submit-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-s-submit-r').classList.add('d-none');
        $('#overlay-body-u-semester').html(data);

    })
});


// update hostel data ajax

$(document).on('submit', '#u-hostel-form-ajax' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/dashboard/authenticate-admin/update-hostel/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

        }



    });
    document.getElementById('submit-text-u-hostel-submit-r').classList.add('d-none');
    document.getElementById('content-loader-u-h-submit-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-h-submit-r').classList.add('d-none');
        $('#overlay-body-u-hostel-data').html(data);

    })
});

// upload deafen list ajax


$(document).on('submit', '#d-l-form-ajax' , function(e){
    e.preventDefault();
    var data = new FormData($('#d-l-form-ajax').get(0));
    req = $.ajax({
        url: '/restricted-url/deafen-maker/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

    });
    document.getElementById('submit-text-d-l').classList.add('d-none');
    document.getElementById('content-loader-d-l').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-d-l').classList.add('d-none');
        $('#overlay-body-deafen-list').html(data);

    })
});

// upload student list ajax

$(document).on('submit', '#s-l-form-ajax' , function(e){
    e.preventDefault();
    var data = new FormData($('#s-l-form-ajax').get(0));
    req = $.ajax({
        url: '/restricted-url/student-maker/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

    });
    document.getElementById('submit-text-s-l').classList.add('d-none');
    document.getElementById('content-loader-s-l').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-s-l').classList.add('d-none');
        $('#overlay-body-student-list').html(data);

    })
});



// submit teacher data form for validation
$(document).on('submit', '#teacher-registration-form-ajax', function(e){
    e.preventDefault();
    var data = new FormData($('#teacher-registration-form-ajax').get(0));

    req = $.ajax({
        url: '/restricted-url/create-teacher-request/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

    });
    document.getElementById('content-loader-t-r-r').classList.remove('d-none')
    document.getElementById("teacher-register-submit-btn").disabled = true;
    document.getElementById('submit-text-t-r-r').classList.add('d-none')
    req.done(function(data){
        $('#overlay-body-r-t').html(data);
    })
});


$(document).on('submit', '#create-student-form-ajax', function(e){
    e.preventDefault();
    var data = new FormData($('#create-student-form-ajax').get(0));

    req = $.ajax({
        type:'POST',
        url:'/restricted-url/register-student/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,
    })

    req.done(function(data){
        $('#overlay-body-r-s').html(data);
    })

})


// for searching transaction student perspective
$(document).on('submit', '#search-transaction-student-option', function(e){
    e.preventDefault();
    var data = new FormData($('#search-transaction-student-option').get(0));
     req = $.ajax({
        type:'POST',
        url:'/restricted-url/search-transaction-student/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,
    });
    req.done(function(data){
        $('#transaction-list-student-option').html(data);
    })
})

