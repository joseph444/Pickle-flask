$(document).ready(function () {
    $('[data-toggle="offcanvas"], #navToggle').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    });
    $(".nav-item").mouseover(function () { 
        $(this).toggleClass('text-dark font-3');
    });
    $(".nav-item").mouseout(function () { 
        $(this).toggleClass('text-dark font-3');
    });
    $(".nav-item").click(
        function(e){
           
            
            $(".nav-item").removeClass("active");
            
            $(this).addClass("active");

        }
    );
});