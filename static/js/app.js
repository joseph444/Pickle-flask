
function preloader(){
    $('#preloader').fadeOut('slow');
}



//navbar settings
$(document).ready(function () {
    $('[data-toggle="offcanvas"], #navToggle').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    });
   $(".nav-item").hover(function () {
           // over
           $(this).removeClass("text-white");
           $(this).toggleClass("text-warning font-3");
       }, function () {
           // out
           $(this).addClass("text-white");
           $(this).toggleClass("text-warning font-3");
       }
   );
});

//changing theme





//Change ImageForm

$(document).ready(function () {
    

    $("#chngimg_form").submit(function (e) { 
        e.preventDefault();
        var form = new FormData(this);
        $("#applyChng").prop("disabled", true);
        $("#applyChng").attr("type","button");
        $('#spinner').show();
        $.ajax({
            type: "POST",
            url: "/change_img",
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                if(response==='1'){
                    location.reload();
                }
                else{
                    alert(response)
                }
                $('#spinner').hide();
            },
            error:
            function(jqXHR, exception){
                alert("Sorry Some Internal Error occured! Please Try Again")
                $('#spinner').hide();
            }
        });
        
    });
    $("#newimg").change(function(e){
        var newUrl=(window.URL||window.webkitURL).createObjectURL(e.target.files[0]);
        
        
        $("#pimg").fadeIn("slow").attr("src",newUrl);
        $("#applyChng").slideDown();

        
    })
});
//template
$(document).ready(function () {
    if($(window).width()<1090 && $(window).width()>500){
        
        $("#groupofbtn").removeClass("btn-group");
    }
    else if($(window).width()<500){
        $("#groupofbtn").removeClass("btn-group");
        
    }
   
    $(window).resize(function () { 
        if($(window).width()<1090 && $(window).width()>500){
           
            $("#groupofbtn").removeClass("btn-group");
        }
        else if($(window).width()<500){
           
            $("#groupofbtn").removeClass("btn-group");
            
        }
    });
});

$(document).ready(
    function () { 
        $("#spinner").hide();
        $("#changetheme").on('shown.bs.modal',function(e){
       var Themes_to_render={
             
            'Original':'nevablue',
            'Spicy':'spicy-tb',
            'Veggies':'veg-tb',
            'Fruity':'fruits-tb',
            'Chilled':'cold-tb',
            'Candy':'candy-tb',
            'Chocolate':'choco-tb',
            'Bread and Butter':'bread-tb',
            'Popsickle':'pop-tb',
            'Sushi':'rice-tb'
        };
        $("#loopForTheme").html("");
        for(Theme in Themes_to_render){
            theme=Themes_to_render[Theme];
            
            template="<div class='card' > <div class='card-body hoverable {1}' id='themeShow' onclick='ChangeTheme(\"{2}\")'> <h4>{2}</h4></div> </div>".replace('{1}',theme);
            template=template.replace("{2}",Theme);
            template=template.replace("{2}",Theme);
            $("#loopForTheme").append(template);
            
            
        }
        })
        
     }
);

function ChangeTheme(value){
    console.log(value);
    
    ChangeTheme=undefined;
    $("#spinner").show()
    NewTheme=value.trim();
    $.ajax({
        type: "GET",
        url: "/change_theme",
        data: {
            'theme':NewTheme
        },
        success:function(e){
            location.reload();
        }
        
    
    });

    
}
$(document).ready(function () {
    $("#toast1").hide();
    $("#descriptionH").change(function(e){
       var newDesc=$(this).val();
       $.ajax({
           type: "GET",
           url: "/change_desc",
           data: {
               'desc':newDesc
           },
          
           success: function (response) {
               
           },
           error:function (param1,param2) {
            console.log(param1.status);
            
             }
       });
       
    })
});

//Search User (for now)

function GetTheFkingTheme(theme){
    var Themes_to_render={
             
        'Original':'nevablue',
        'Spicy':'spicy-rl',
        'Veggies':'veg-rl',
        'Fruity':'fruits-rl',
        'Chilled':'cold-rl',
        'Candy':'candy-rl',
        'Chocolate':'choco-rl',
        'Bread and Butter':'bread-rl',
        'Popsickle':'pop-rl',
        'Sushi':'rice-rl'
    };
    return Themes_to_render[theme];
}

$(document).ready(
    function () { 
        $("#searchBtn").click(function(){
            var SearchValue=$("#searchInpt").val();
            if(SearchValue===''){
                $("#searchInpt").addClass('is-invalid');
                setTimeout(() => {
                    $("#searchInpt").removeClass('is-invalid')
                }, 2000);
            }
            else{
                        var spinners='<div >\
                        <div class="spinner-grow text-muted"></div>\
                        <div class="spinner-grow text-primary"></div>\
                        <div class="spinner-grow text-success"></div>\
                        <div class="spinner-grow text-info"></div>\
                        <div class="spinner-grow text-warning"></div>\
                        <div class="spinner-grow text-danger"></div>\
                        <div class="spinner-grow text-secondary"></div>\
                        <div class="spinner-grow text-dark"></div>\
                        <div class="spinner-grow text-light"></div>\
                    </div>';
                    $('#searchResult').html(spinners);
                $.ajax({
                    type: "POST",
                    url: "/search",
                    data: {
                        search:$("#searchInpt").val()
                    },
                    success: function (response) {
                        $("#searchInpt").val("")
                        
                        $("#searchResult").html("");
                        
                        $("#searchResult").append("<h1 class='text-center display-3'>Your Search Result</h1> <hr> ")
                        var i=true;
                        for(var k in response){
                            i=false;
                            var template='<li class="list-group-item {theme}" onclick="location.replace(\'/profile/{id}\')"><div class="media  my-3">\
                            <div class="profile-img-side">\
                                            <a class="d-flex" href="/profile/{id}" class="">\
                                                <img src="{pimg}" alt="">\
                                            </a> </div>\
                                            <div class="media-body" style="word-break: break-all;" onclick="location.replace(\'/profile/{id}\')">\
                                                <h4>{name}</h4>\
                                                \
                                            </div></div>\
                                        </li>';
                            var Person=response[k];
                            var Id=Person.Id;
                            var Name=Person.Username;
                            var Pimg=Person.Pimg;
                            var Theme=GetTheFkingTheme(Person.Theme);
                            template=template.replace('{theme}',Theme);
                            template=template.replace('{id}',Id);
                            template=template.replace('{pimg}',Pimg);
                            template=template.replace('{name}',Name);
                            $('#searchResult').append(template);
                            
                            
                        }
                        console.log(i);
                        if(i){
                            $('#searchResult').append("<h4>Sorry We did not Found the user <span><i class='fa fa-frown-o' aria-hidden='true'></i></span></h4>");
                        }
                    }
                });
            }

        });
     }
);



//Post

//submission of post

$(document).ready(function () {
    $("#posttype").change(function (e) { 
        e.preventDefault();
        var postType=e.target.value;
        if(postType==='Recipie'){
            $("#recipie").fadeIn("slow");
            $("#rate").fadeOut("fast");
        }
        else if(postType==='Rating'){
            $("#recipie").fadeOut("fast");
            $("#rate").fadeIn("slow");
        }
        else{
            $("#recipie").fadeOut("fast");
            $("#rate").fadeOut("slow");
        }
        
    });
});

$(document).ready(
    function () { 
        var gliders=document.querySelectorAll('.glider');
        for(var i=0;i<gliders.length;i++){
            new Glider(gliders[i], {
                slidesToShow: 1,
                draggable: true,
                arrows: {
                  prev: '.glider-prev',
                  next: '.glider-next'
                }
              });
        }

        
        
     }

);

function Like(id){
    var likeBtnText=$('#likeTxt').text();
    var unlikeBtnText=$('#unlikeTxt').text();
    if(likeBtnText==='Like'){
        $('#likeTxt').text("Liked");
    }
    else if (likeBtnText==='Liked'){
        $('#likeTxt').text("Like")
    }
    sendLikerqst(id);
    if(unlikeBtnText==='Unliked'){
        $('#unlikeTxt').text("Unlike");
        sendunlikerqst(id);
    }
    
}
function Unlike(id){
    var likeBtnText=$('#likeTxt').text();
    var unlikeBtnText=$('#unlikeTxt').text();
    if(unlikeBtnText==='Unlike'){
        $('#unlikeTxt').text("Unliked");
    }
    else if(unlikeBtnText==='Unliked'){
        $('#unlikeTxt').text("UnLike");
    }
    sendunlikerqst(id);

    if(likeBtnText==='Liked'){
        $('#likeTxt').text("Like")
        sendLikerqst(id);
    }
}

function sendLikerqst(id){
    $.ajax({
        type: "POST",
        url: "/post/like",
        data: {
            id:id
        },
        success:function (response) {
            console.log(response);
            
        }
    });

}
function sendunlikerqst(id){
    $.ajax({
        type: "POST",
        url: "/post/unlike",
        data: {
            id:id
        },
        success:function (response) {
            console.log(response);
            
        }
    });
}
