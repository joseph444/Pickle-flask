
var socketio=io();
socketio.on('recvmsg', function (param) { 
    room=param['id'];
    var arr=location.pathname.split('/');
    if(!arr.some(function(value){return value=='message'})){
        alert('You have New Message From '+param['un']);
    }
    
    else{
        $.ajax({
            type: "GET",
            url: "/chats",
            success: function (response) {
                changeListOfMessages(response);
            }
        });
        
    }
 });


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
             
            'Original':'Original',
            'Spicy':'Spicy',
            'Veggies':'Veggies',
            'Fruity':'Fruity ',
            'Chilled':'Chilled',
            'Candy':'Candy',
            'Chocolate':'Chocolate',
            'Bread and Butter':'Bread-and-Butter',
            'Popsickle':'Popsickle',
            'Sushi':'Sushi'
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
        'Original':'Original',
        'Spicy':'Spicy',
        'Veggies':'Veggies',
        'Fruity':'Fruity ',
        'Chilled':'Chilled',
        'Candy':'Candy',
        'Chocolate':'Chocolate',
        'Bread and Butter':'Bread-and-Butter',
        'Popsickle':'Popsickle',
        'Sushi':'Sushi'
    };
    return Themes_to_render[theme];
}

$(document).ready(
    function () { 
        $("#searchInpt").keyup(function (e) {
            if(e.which===13) {
                console.log(13);
                
                $("#searchBtn").click();
            }
            
        });

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
var CUID;
async function getCurrentUser(){
    var response = await fetch("/get_current_user");
    var data=await response.json();
    CUID=data;
    
    
}
getCurrentUser();

function Like(id){
    
    sendLikerqst(id);
}
function Unlike(id){

    sendunlikerqst(id);
}
function addComment(id){
    var comment= $('#add-comment-'+id).val();
    comment=comment.trim();
    console.log("Working");
    

    if(comment===''){
        $('#comment-'+id).addClass('is-invalid');
        console.log("Working1");
        return;

    }
    $.ajax({
        type: "POST",
        url: "/post/comment",
        data: {
            id:id,
            comment:comment
        },
        success:function (response) {
           
           
            var no= parseInt( $('#no-comment-'+id).text());
           if(response!='-1'||response!='-2'||response!='-3'){
            $('#no-comment-'+id).text(no+1);
            $('#add-comment-'+id).val(" ")
            $('#comment-'+id).hide();
            
            $("#comments").html("");
            var key=1;
            for(var k in response){
                var comment=response[k]['comment'];
                var time=response[k]['time'];
                var user=response[k]['user'];
                var userid=user['Id'];
                var username=user['Username'];
                var Pimg=user['Pimg'];

               
                if(CUID==userid){
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\
                                    </a>\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <span class="float-right btn" >\
                                   <button class="btn" onclick="deleteComment('{postid}','{key}')"> <i class="fa fa-trash" aria-hidden="true"></i></button>  </a>\ 
                                   <button class="btn" onclick="$('#updatecmnt-{key},.hide-on-update-{key}').fadeToggle()"> <i class="fa fa-pencil" aria-hidden="true"></i> </button>\
                             </h5>\
                             <div class="form-inline mb-0" id="updatecmnt-{key}" style="display: none;">\
                                    <input type="text" name="comment" id="update-comment-{postid}" class="add-comment form-control form-control-lg mx-2" value="{comment}" style="width: 80%;height:2.3rem!important;background-color:#818181" placeholder="Add Comment">\
                                    <span><button class="btn btn-dark" onclick="EditComment('{postid}','{key}')"> <i class="fa fa-paper-plane" aria-hidden="true"></i> </button></span>\
                            </div>\
                            <div class="hide-on-update-{key}">\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>
                               </div>   \
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                else{
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <a class="float-right btn" href="#" data-toggle="dropdown" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa fa-ellipsis-v" aria-hidden="true" ></i>  </a>\ 
                             </h5>\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>\
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                
                
                template=template.replace('{userid}',userid);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{postid}",id);
                template=template.replace("{postid}",id);
                template=template.replace("{postid}",id);
                template=template.replace("{postid}",id);
                template=template.replace("{postid}",id);
                template=template.replace('{pimg}',Pimg);
                template=template.replace('{username}',username);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{time}',time);
                
                $("#comments").append(template);
                key+=1;
            }
           }
           
           
            
        }
    });
}

function sendLikerqst(id){
    
    $.ajax({
        type: "POST",
        url: "/post/like",
        data: {
            id:id
        },
        success:function (response) {
            var no= parseInt( $('#nooflikes-'+id).text());
           if(response==='added'){
               
               $('#nooflikes-'+id).text(no+1);
           }
           else if(response==='removed'){
            $('#nooflikes-'+id).text(no-1);
           }
           else{
               var noo=parseInt($('#noofDislikes-'+id).text())
               $('#nooflikes-'+id).text(no+1);
               $('#noofDislikes-'+id).text(noo-1);
           }
            
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
            var no=parseInt($('#noofDislikes-'+id).text());
            if(response==='added'){
               
                $('#noofDislikes-'+id).text(no+1);
            }
            else if(response==='removed'){
             $('#noofDislikes-'+id).text(no-1);
            }
            else{
                var noo=parseInt($('#nooflikes-'+id).text())
                $('#noofDislikes-'+id).text(no+1);
                $('#nooflikes-'+id).text(noo-1);
            }
            
        }
    });
}

function deleteComment(postid,key){
    $.ajax({
        type: "POST",
        url: "/post/comment/delete",
        data: {
            id:parseInt( postid),
            comid:parseInt( key)
        },
        
        success: function (response) {
            if(response!='error'){
                var no= parseInt( $('#no-comment-'+postid).text());
          
            $('#no-comment-'+postid).text(no-1);
            $('#add-comment-'+postid).val(" ")
            $('#comment-'+postid).hide();
                $("#comments").html("");
            var key=1;
            for(var k in response){
                var comment=response[k]['comment'];
                var time=response[k]['time'];
                var user=response[k]['user'];
                var userid=user['Id'];
                var username=user['Username'];
                var Pimg=user['Pimg'];

               
                if(CUID==userid){
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\
                                    </a>\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <span class="float-right btn" >\
                                   <button class="btn" onclick="deleteComment('{postid}','{key}')"> <i class="fa fa-trash" aria-hidden="true"></i></button>  </a>\ 
                                   <button class="btn" onclick="$('#updatecmnt-{key},.hide-on-update-{key}').fadeToggle()"> <i class="fa fa-pencil" aria-hidden="true"></i> </button>\
                             </h5>\
                             <div class="form-inline mb-0" id="updatecmnt-{key}" style="display: none;">\
                                    <input type="text" name="comment" id="update-comment-{postid}" class="add-comment form-control form-control-lg mx-2" value="{comment}" style="width: 80%;height:2.3rem!important;background-color:#818181" placeholder="Add Comment">\
                                    <span><button class="btn btn-dark" onclick="EditComment('{postid}','{key}')"> <i class="fa fa-paper-plane" aria-hidden="true"></i> </button></span>\
                            </div>\
                            <div class="hide-on-update-{key}">\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>
                               </div>   \
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                else{
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <a class="float-right btn" href="#" data-toggle="dropdown" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa fa-ellipsis-v" aria-hidden="true" ></i>  </a>\ 
                             </h5>\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>\
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                
                
                template=template.replace('{userid}',userid);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{postid}",postid);
                template=template.replace("{postid}",postid);
                template=template.replace("{postid}",postid);
                template=template.replace("{postid}",postid);
                template=template.replace('{pimg}',Pimg);
                template=template.replace('{username}',username);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{time}',time);
                
                $("#comments").append(template);
                key+=1;
            }
            }
            
        }
    });
}

function DelPost(postId){
    $.ajax({
        type: "POST",
        url: "/post/delete",
        data: {
            id:postId
        },
        
        success: function (response) {
            if(response!='error'){
                location.reload();
            }
        }
    });
}
function EditComment(posid,com){
    var comment=$("#update-comment-"+posid).val().trim();
    if(comment==''){
        $("#update-comment-"+posid).addClass('is-invalid');
        return ;
    }
    $.ajax({
        type: "POST",
        url: "comment/update",
        data: {
            id:posid,
            comid:com,
            comment:comment
        },
        success: function (response) {
            if(response!='error'){
                
                $("#comments").html("");
            var key=1;
            for(var k in response){
                var comment=response[k]['comment'];
                var time=response[k]['time'];
                var user=response[k]['user'];
                var userid=user['Id'];
                var username=user['Username'];
                var Pimg=user['Pimg'];

               
                if(CUID==userid){
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\
                                    </a>\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <span class="float-right btn" >\
                                   <button class="btn" onclick="deleteComment('{postid}','{key}')"> <i class="fa fa-trash" aria-hidden="true"></i></button>  </a>\ 
                                   <button class="btn" onclick="$('#updatecmnt-{key},.hide-on-update-{key}').fadeToggle()"> <i class="fa fa-pencil" aria-hidden="true"></i> </button>\
                             </h5>\
                             <div class="form-inline mb-0" id="updatecmnt-{key}" style="display: none;">\
                                    <input type="text" name="comment" id="update-comment-{postid}" class="add-comment form-control form-control-lg mx-2" value="{comment}" style="width: 80%;height:2.3rem!important;background-color:#818181" placeholder="Add Comment">\
                                    <span><button class="btn btn-dark" onclick="EditComment('{postid}','{key}')"> <i class="fa fa-paper-plane" aria-hidden="true"></i> </button></span>\
                            </div>\
                            <div class="hide-on-update-{key}">\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>
                               </div>   \
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                else{
                    var template=`\
                <div class="list-group-item">\
                <div class="container">\
                \
                <div class="media">\
                                <a href="/profile/{userid}">\
                                    <img class="align-self-center mr-3 " src="{pimg}" style="border-radius: 50%;background-color:#4f4f4f;width:4rem;height:4rem">\ 
                                <div class="media-body">\
                                  <h5 class="mt-0">{username} <a class="float-right btn" href="#" data-toggle="dropdown" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa fa-ellipsis-v" aria-hidden="true" ></i>  </a>\ 
                             </h5>\
                                  <p>{comment}</p>\
                                  <p class="mb-0 text-muted" style='font-size:8px'>Time of comment: {time}</p>\
                                </div>\
                              </div>\
                            </div>  \
                </div>`;
                }
                
                
                template=template.replace('{userid}',userid);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{key}",key);
                template=template.replace("{postid}",posid);
                template=template.replace("{postid}",posid);
                template=template.replace("{postid}",posid);
                template=template.replace("{postid}",posid);
                template=template.replace("{postid}",posid);
                template=template.replace('{pimg}',Pimg);
                template=template.replace('{username}',username);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{comment}',comment);
                template=template.replace('{time}',time);
                
                $("#comments").append(template);
                key+=1;
            }
            }
            
        }
    });
}
function pin(postid){

    $.ajax({
        type: "POST",
        url: "/pinned/add",
        data: {
            id:postid
        },
        success: function (response) {
            if(response=='added'){
                alert('This Post is added to your Pin Board.');
            }
            else if(response=='remove'){
                alert('This Post is removed from your Pin Board.');
            }
            else{
                console.log("error");
                
            }
            
        }
    });
}