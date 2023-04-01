
// search tabulation sheet ajax
$(document).on('submit', '#search-tabulation-sheet-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url: '/dashboard/college-private-links/tabulation-sheet-filter/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            session: $('#session').val(),
            department:$('#id_department').val(),
            semester: $('#id_semester').val(),

        }


    });
    req.done(function(data){

        $('#s-tab-body').html(data);
    })
});


//loader-d-c-g-tab-t

$(document).on('click', '.link-btn', function(e){
    e.preventDefault();
    var get_attr = $(this).attr('btn_no');

    if (get_attr === '1'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/college-private-links/get-template-link/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-tab-t').classList.remove('d-none');
        req.done(function(data){
             ele = document.getElementById('t-link-btn1').classList.add('active');
             ele = document.getElementById('t-link-btn2').classList.remove('active');
             document.getElementById('t-link-btn4').classList.remove('active');
             document.getElementById('t-link-btn3').classList.remove('active');
             document.getElementById('loader-d-c-g-tab-t').classList.add('d-none');

             $('#tabulation_content').html(data);
        })
    }
    else if (get_attr === '2'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/college-private-links/get-template-link/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-tab-t').classList.remove('d-none');
        req.done(function(data){
             document.getElementById('t-link-btn1').classList.remove('active');
             document.getElementById('t-link-btn2').classList.add('active');
             document.getElementById('t-link-btn4').classList.remove('active');
             document.getElementById('t-link-btn3').classList.remove('active');
             document.getElementById('loader-d-c-g-tab-t').classList.add('d-none');

             $('#tabulation_content').html(data);
        })
    }


    else if (get_attr === '3'){
        req = $.ajax({
            type:'POST',
            url:'/dashboard/college-private-links/get-template-link/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-tab-t').classList.remove('d-none');

        req.done(function(data){

             document.getElementById('t-link-btn1').classList.remove('active');
             document.getElementById('t-link-btn2').classList.remove('active');
             document.getElementById('t-link-btn4').classList.remove('active');
             document.getElementById('t-link-btn3').classList.add('active');
             document.getElementById('loader-d-c-g-tab-t').classList.add('d-none');

             $('#tabulation_content').html(data);
        })
    }
     else if (get_attr === '4'){
        req = $.ajax({
            type:'POST',
            url:'/dashboard/college-private-links/get-template-link/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-d-c-g-tab-t').classList.remove('d-none');

        req.done(function(data){

             document.getElementById('t-link-btn1').classList.remove('active');
             document.getElementById('t-link-btn2').classList.remove('active');
             document.getElementById('t-link-btn3').classList.remove('active');
             document.getElementById('t-link-btn4').classList.add('active');
             document.getElementById('loader-d-c-g-tab-t').classList.add('d-none');

             $('#tabulation_content').html(data);
        })
    }

})


// search mark sheet ajax
$(document).on('submit', '#search-mark-sheet-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url: '/dashboard/college-private-links/mark-sheet-filter/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            session: $('#session').val(),
            department:$('#id_department').val(),
            semester: $('#id_semester').val(),

        }


    });
    req.done(function(data){

        $('#s-tab-body').html(data);
    })
});

// search short mark sheet ajax

$(document).on('submit', '#search-short-mark-sheet-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url: '/dashboard/college-private-links/short-mark-sheet-filter/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            session: $('#session').val(),
            department:$('#id_department').val(),
            semester: $('#id_semester').val(),

        }


    });
    req.done(function(data){

        $('#s-tab-body').html(data);
    })
});


// search to edit result ajax

$(document).on('submit', '#search-to-edit-page-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url: '/dashboard/college-private-links/search-to-edit-result-sheet/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            roll: $('#roll').val(),
            session: $('#session').val(),
            department:$('#id_department').val(),
            semester: $('#id_semester').val(),

        }


    });
    req.done(function(data){

        $('#s-tab-body').html(data);
    })
});

