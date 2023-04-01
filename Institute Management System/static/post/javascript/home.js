// nav bar javascript




function routineF(){
    var ele = document.getElementById('e-semesters');
    var result = document.getElementById('r-semesters');
    var eit = document.getElementById('result-i-t');
    eit.classList.remove('t-bg');

    ele.classList.toggle('r-disable');
}



function ebg(){
    var ele = document.getElementById('exam-i-t');
    ele.classList.toggle('t-bg')
}

function myFunction() {
            
    var element = document.getElementById("toggle-nav");
    element.classList.toggle("disable");
}


// nav bar javascript end 


//container

function sideroutineF(){
    var ele = document.getElementById('side-e-semesters');
    var result = document.getElementById('side-r-semesters');
    var eit = document.getElementById('side-result-i-t');
    eit.classList.remove('side-bg');
    result.classList.remove('side-disable');
    ele.classList.toggle('side-disable');
}


function sideresultF(){
    var ele = document.getElementById('side-r-semesters');
    var routine = document.getElementById('side-e-semesters');
    routine.classList.remove('side-disable');
    var rit = document.getElementById('side-exam-i-t');

    rit.classList.remove('side-bg');
    ele.classList.toggle('side-disable');
}



function srbg(){
    var element = document.getElementById('side-result-i-t');
    element.classList.toggle('side-bg')
}

function sebg(){
    var ele = document.getElementById('side-exam-i-t');
    ele.classList.toggle('side-bg')
}

// container main

function odots(){
    var dot = document.getElementById('toggle-option');
    dot.classList.toggle('o-t-eneble')
    
}

function readMore(){
    var readmore = document.getElementsByClassName('see-more')[0];
    
    readmore.classList.toggle('d-show');

    var rmb = document.getElementsByClassName('read-more-btn')[0];
    rmb.classList.toggle('d-none');

    var seeless = document.getElementsByClassName('see-less')[0];

    seeless.classList.add('d-show')

}

function readLess(){
    var readmore = document.getElementsByClassName('see-more')[0];
    
    readmore.classList.remove('d-show');

    var rmb = document.getElementsByClassName('read-more-btn')[0];
    rmb.classList.remove('d-none');
    var seeless = document.getElementsByClassName('see-less')[0];

    seeless.classList.remove('d-show')
}




function likebutton(){
    var like = document.getElementsByClassName('like-btn')[0];
    like.classList.toggle('like-btn-toggle')
}


