$(document).on('submit', '#search-transactions-form', function(e){
    e.preventDefault();

    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/transaction-home/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword:$('#keyword').val(),

        }

    });
    req.done(function(data){

         $('#transaction-recipients').html(data);
    })
})

// custom transaction form ajax

$(document).on('submit', '#create-custom-transaction-form', function(e){

    e.preventDefault();
    var data = new FormData($('#create-custom-transaction-form').get(0));

    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/create-custom-transaction/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,



    });
    document.getElementById('submit-text-c-c-trans').classList.add('d-none');
    document.getElementById('content-loader-c-c-tra').classList.remove('d-none');
    req.done(function(data){
         document.getElementById('content-loader-c-c-tra').classList.add('d-none');
         $('#overlay-body-make-c-trans').html(data);
    })
})

// ajax for changing the page route and content.

$(document).on('click', '.link-btn-trans', function(e){
    e.preventDefault();
    var get_attr = $(this).attr('btn_no');

    if (get_attr === '1'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/transaction/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-t-c-g-t').classList.remove('d-none');
        req.done(function(data){
             ele = document.getElementById('link-btn4').classList.add('active');
             ele = document.getElementById('link-btn5').classList.remove('active');
             ele = document.getElementById('link-btn6').classList.remove('active');
             document.getElementById('loader-t-c-g-t').classList.add('d-none');

             $('#transaction_contents').html(data);
        })
    }
    else if (get_attr === '2'){

        req = $.ajax({
            type:'POST',
            url:'/dashboard/transaction/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-t-c-g-t').classList.remove('d-none');
        req.done(function(data){
             ele = document.getElementById('link-btn4').classList.remove('active');
             ele = document.getElementById('link-btn5').classList.add('active');
             ele = document.getElementById('link-btn6').classList.remove('active');
             document.getElementById('loader-t-c-g-t').classList.add('d-none');

             $('#transaction_contents').html(data);
        })
    }
    else if (get_attr === '3'){
        req = $.ajax({
            type:'POST',
            url:'/dashboard/transaction/get-link-template/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                link_id:get_attr,
            }

        });
        document.getElementById('loader-t-c-g-t').classList.remove('d-none');

        req.done(function(data){

             ele = document.getElementById('link-btn4').classList.remove('active');
             ele = document.getElementById('link-btn5').classList.remove('active');
             ele = document.getElementById('link-btn6').classList.add('active');
             document.getElementById('loader-t-c-g-t').classList.add('d-none');

             $('#transaction_contents').html(data);
        })
    }

})


// js for filter toggle



function show_filter_toggle(){
    var ele = document.getElementById('filter-toggle');
    ele.classList.toggle('d-none')
}


// js for adding new element to html

function add_new_node(){

    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/get-extra-reason-template/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

        }
    });
    req.done(function(data){
        var ele = document.getElementById('add-new-node-btn');
        ele.insertAdjacentHTML("beforebegin",data )

    })
}

// ajax for other reason in custom transaction

$(document).ready(function(){

     $('#id_transaction_reason').on('change', function(){
            var selectedEle = $(this).children("option:selected").val();

            if (selectedEle=='Others'){
                let ele = document.getElementById('for-other-selection');
                ele.insertAdjacentHTML('afterend', '<div class="input" id="other_reason"><span> Reason  :</span> <input name="other_reason" placeholder="Enter other reason . . ." type="text"></div>' )

            }
            else{
                try{
                    let ele = document.getElementById('other_reason');
                    ele.classList.add('d-none')
                }
                catch{

                }


            }
        })
})

// for test


// for statement filter

$(document).on('submit', '#statement_filter', function(e){
    e.preventDefault();
    var data = new FormData($('#statement_filter').get(0));
    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/get-statement/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,



    });
    document.getElementById('submit-text-search-statement').classList.add('d-none');
    document.getElementById('content-loader-search-statement').classList.remove('d-none');
    req.done(function(data){
         document.getElementById('content-loader-search-statement').classList.add('d-none');
         $('#overlay-body-get-statement').html(data);
    })

})

// for querying student in custom transaction form

$(document).on('submit', '#query-student-data-c-trans', function(e){
    e.preventDefault();
    var data = new FormData($('#query-student-data-c-trans').get(0));
    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/query-student-arrears-data/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,



    });
    document.getElementById('submit-text-q-s-c-trans').classList.add('d-none');
    document.getElementById('content-loader-q-s-c-tra').classList.remove('d-none');
    req.done(function(data){
         document.getElementById('content-loader-q-s-c-tra').classList.add('d-none');
         document.getElementById('submit-text-q-s-c-trans').classList.remove('d-none');
         $('#query-student-c-trans-data').html(data);
    })
})


// for refreshing custom transaction form
function location_reload(){
    req = $.ajax({
        type:'get',
        url:'/dashboard/transaction/refresh-c-trans/',

    });
    req.done(function(data){
        $('#overlay-body-make-c-trans').html(data);
    })
}
// for transaction statement

$(document).on('submit', '#transaction-statement', function(e){
    e.preventDefault();
    var data = new FormData($('#transaction-statement').get(0));
    req = $.ajax({
        type:'POST',
        url:'/dashboard/transaction/get-transaction-statement-by-time-range-request/',
        data:data,
        cache: false,
        processData: false,
        contentType: false,



    });
    document.getElementById('submit-text-search-trans-statement').classList.add('d-none');
    document.getElementById('content-loader-search-trans-statement').classList.remove('d-none');
    req.done(function(data){
         document.getElementById('content-loader-search-trans-statement').classList.add('d-none');
         document.getElementById('submit-text-search-trans-statement').classList.remove('d-none');
         $('#overlay-body-transaction-statement').html(data);
    })
})