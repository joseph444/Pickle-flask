
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

$(document).ready(function () {
    var Themes={
             
                'Original':'nevablue',
                'Spicy':'spicy-',
                'Veggies':'veg-',
                'Fruity':'fruits-',
                'Chilled':'cold-',
                'Candy':'candy-',
                'Chocolate':'choco-',
                'Bread and Butter':'bread-',
                'Popsickle':'pop-',
                'Sushi':'rice-'
    };

    var OldTheme=$('#chngThm').val();
    
    var ArrayOfrl=$('.'+Themes[OldTheme]+'rl');
    var ArrayOftb=$('.'+Themes[OldTheme]+'tb');
        $('#chngThm').change(function (e) { 
            
            e.preventDefault();
            let NewTheme=e.target.value;
            
            
            $.ajax({
                type: "GET",
                url: "/change_theme",
                data: {
                    'theme':NewTheme
                },
                success:function(e){
                    var newthemeclass=Themes[e];
                    var oldthemeclass=Themes[OldTheme];
                   
                    if(e==='Original'){
                        var rl=newthemeclass;
                        var tb=newthemeclass;
                        
                    }
                    else{
                        var rl=newthemeclass+'rl';
                        var tb=newthemeclass+'tb';
                        
                    }
                        
                    if(OldTheme==='Original'){
                        $(ArrayOfrl).removeClass(oldthemeclass);
                    $(ArrayOftb).removeClass(oldthemeclass);
                    }
                    else{
                        $(ArrayOfrl).removeClass(oldthemeclass+'rl');
                        $(ArrayOftb).removeClass(oldthemeclass+'tl');
                    }
                   
                    $(ArrayOfrl).addClass(rl);
                    $(ArrayOftb).addClass(rl);
                    OldTheme=e;
                    $('#ThemeName').text(OldTheme);
                    
                    
                }
                
            
            });
            console.log(OldTheme);
    
        });
        
});

$(document).ready(function () {
    var Themes={
             
                'Original':'nevablue',
                'Spicy':'spicy-',
                'Veggies':'veg-',
                'Fruity':'fruits-',
                'Chilled':'cold-',
                'Candy':'candy-',
                'Chocolate':'choco-',
                'Bread and Butter':'bread-',
                'Popsickle':'pop-',
                'Sushi':'rice-'
    };

    var OldTheme=$('#chngThm1').val();
    
    var ArrayOfrl=$('.'+Themes[OldTheme]+'rl');
    var ArrayOftb=$('.'+Themes[OldTheme]+'tb');
        $('#chngThm1').change(function (e) { 
            
           
            let NewTheme=e.target.value;
            
            
            $.ajax({
                type: "GET",
                url: "/change_theme",
                data: {
                    'theme':NewTheme
                },
                success:function(e){
                    var newthemeclass=Themes[e];
                    var oldthemeclass=Themes[OldTheme];
                   
                    if(e==='Original'){
                        var rl=newthemeclass;
                        var tb=newthemeclass;
                        console.log(rl); 
                    }
                    else{
                        var rl=newthemeclass+'rl';
                        var tb=newthemeclass+'tb';
                        
                    }
                         
                    if(OldTheme==='Original'){
                        $(ArrayOfrl).removeClass(oldthemeclass);
                    $(ArrayOftb).removeClass(oldthemeclass);
                    }
                    else{
                        $(ArrayOfrl).removeClass(oldthemeclass+'rl');
                        $(ArrayOftb).removeClass(oldthemeclass+'tl');
                    }
                   
                    $(ArrayOfrl).addClass(rl);
                    $(ArrayOftb).addClass(rl);
                    OldTheme=e;

                    $('#ThemeName1').text(OldTheme);
                    
                    
                }
                
            
            });
            console.log(OldTheme);
    
        });
        
});


//Change ImageForm

$(document).ready(function () {
    $('#spinner1').hide();

    $("#chngimg_form").submit(function (e) { 
        e.preventDefault();
        var form = new FormData(this);
        $("#applyChng").prop("disabled", true);
        $("#applyChng").attr("type","button");
        $('#spinner1').show();
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
                $('#spinner1').hide();
            },
            error:
            function(jqXHR, exception){
                alert("Sorry Some Internal Error occured! Please Try Again")
                $('#spinner1').hide();
            }
        });
        
    });
    $("#newimg").change(function(e){
        var newUrl=(window.URL||window.webkitURL).createObjectURL(e.target.files[0]);
        
        
        $("#pimg").fadeIn("slow").attr("src",newUrl);
        $("#applyChng").slideDown();
        
    })
});