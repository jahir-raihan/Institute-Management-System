// overlay js
function on_universal(overlay){
    document.getElementById(overlay).style.display = "block";
    document.getElementById('body').classList.add('scroll-disable')
}
function off_universal(overlay){
    document.getElementById(overlay).style.display = "none";
    document.getElementById('body').classList.remove('scroll-disable')
    location.reload()
}






$(document).on('submit', '#search-students', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/dashboard/college-user-system/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword-student').val(),

        }

    });
    document.getElementById('loader-d-c-s-s').classList.remove('d-none');
    req.done(function(data){
          document.getElementById('loader-d-c-s-s').classList.add('d-none');

         $('#query-student').html(data);
    })
})



// semester system ajax

$(document).on('submit', '#search-semester-students-dashboard', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/dashboard/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#d-semester-students').html(data);
    })
})
//loader-d-c-g-t

$(document).on('click', '.link-btn', function(e){
    e.preventDefault();
    var get_attr = $(this).attr('btn_no');

    if (get_attr === '1'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-t').classList.remove('d-none');
        req.done(function(data){
             ele = document.getElementById('link-btn1').classList.add('active');
             ele = document.getElementById('link-btn2').classList.remove('active');
             ele = document.getElementById('link-btn3').classList.remove('active');
             document.getElementById('loader-d-c-g-t').classList.add('d-none');

             $('#dashboard_contents').html(data);
        })
    }
    else if (get_attr === '2'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-t').classList.remove('d-none');
        req.done(function(data){
             ele = document.getElementById('link-btn1').classList.remove('active');
             ele = document.getElementById('link-btn2').classList.add('active');
             ele = document.getElementById('link-btn3').classList.remove('active');
             document.getElementById('loader-d-c-g-t').classList.add('d-none');

             $('#dashboard_contents').html(data);
        })
    }
    else if (get_attr === '3'){
        req = $.ajax({
            type:'POST',
            url:'/dashboard/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-t').classList.remove('d-none');

        req.done(function(data){

             ele = document.getElementById('link-btn1').classList.remove('active');
             ele = document.getElementById('link-btn2').classList.remove('active');
             ele = document.getElementById('link-btn3').classList.add('active');
             document.getElementById('loader-d-c-g-t').classList.add('d-none');

             $('#dashboard_contents').html(data);
        })
    }

})




// dashboard hostel student ajax

id="d-semester-students"

$(document).on('submit', '#search-hostel-students-dashboard', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/dashboard/hostel-system/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#d-hostel-students').html(data);
    })
})


// Register teacher ajax
$(document).on('submit', '#c-c-with-data-t-r-f', function(e){
    e.preventDefault();
    var data = new FormData($('#c-c-with-data-t-r-f').get(0));
    req = $.ajax({
        type:'POST',
        url:'/restricted-url/create-teacher/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,


    });
    req.done(function(data){

        $('#overlay-body-r-t').html(data);


    })
});


// update midterm fee ajax
$(document).on('submit', '#u-mid-term-form-ajax' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/semester-system/college-private-links/update-midterm-fee-info/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
        }



    });
    document.getElementById('submit-text-u-mid-submit-r').classList.add('d-none');
    document.getElementById('content-loader-u-mid-submit-r').classList.remove('d-none');

    req.done(function(data){
        if (data=='False'){
            $('#overlay-body-u-mid-fee').html('<p style="color:#ff8800;text-align:center;">Bad Request</p>');
        }
        document.getElementById('content-loader-u-mid-submit-r').classList.add('d-none');
        $('#overlay-body-u-mid-fee').html(data);

    })
});


// authenticate admin for midterm fee  ajax
$(document).on('submit', '#u-mid-term-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/semester-system/college-private-links/authenticate-admin-user/',
        type: 'POST',
        data: {
            password:$('#mid-u-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#mid-u-auth-email').val()
        }



    });
    document.getElementById('submit-text-u-mid-fee-r').classList.add('d-none');
    document.getElementById('content-loader-u-m-f-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-m-f-r').classList.add('d-none');

        $('#overlay-body-u-mid-fee').html(data);
    })
})


// update registration fee ajax
$(document).on('submit', '#u-reg-form-ajax' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/semester-system/college-private-links/update-reg-fee-info/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            amount:$('#amount').val(),
        }



    });
    document.getElementById('submit-text-u-reg-submit-r').classList.add('d-none');
    document.getElementById('content-loader-u-reg-submit-r').classList.remove('d-none');

    req.done(function(data){
        if (data=='False'){
            $('#overlay-body-u-reg-fee').html('<p style="color:#ff8800;text-align:center; height:200px; margin-top:35%;">Bad Request</p>');
        }
        document.getElementById('content-loader-u-reg-submit-r').classList.add('d-none');
        $('#overlay-body-u-reg-fee').html(data);

    })
});
// authenticate admin for registration fee ajax

$(document).on('submit', '#u-reg-authenticate-form' , function(e){
    e.preventDefault();
    req = $.ajax({
        url: '/semester-system/college-private-links/authenticate-admin-user-reg/',
        type: 'POST',
        data: {
            password:$('#reg-u-auth-pass').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#reg-u-auth-email').val()
        }



    });
    document.getElementById('submit-text-u-reg-fee-r').classList.add('d-none');
    document.getElementById('content-loader-u-r-f-r').classList.remove('d-none');

    req.done(function(data){
        document.getElementById('content-loader-u-r-f-r').classList.add('d-none');

        $('#overlay-body-u-reg-fee').html(data);
    })
})
// for adding previous semester data of a student

$(document).on('submit', '#add_prev_semester_data' , function(e){
    e.preventDefault();
    var data = new FormData($('#add_prev_semester_data').get(0));
    req = $.ajax({
        type:'POST',
        url:'/semester-system/college-private-links/add-prev-semester-data/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,
    });
    document.getElementById('submit-text-a-prev-s-data').classList.add('d-none');
    document.getElementById('content-loader-add-prev-s-data').classList.remove('d-none');
    req.done(function(data){
    document.getElementById('content-loader-add-prev-s-data').classList.add('d-none');
        $('#overlay-body-add-prev-semester-data').html(data);
    })

})


// for refreshing the add prev semester data form

function s_location_reload(){
    req = $.ajax({
        type:'GET',
        url:'/semester-system/college-private-links/refresh-add-prev-semester-data/',

    });
    req.done(function(data){
        $('#overlay-body-add-prev-semester-data').html(data);
    })
}