$(function() {
    $("#friend").click(function(event) {
        console.log("please");
        event.preventDefault();
        var this_ = $(this)
        var friendUrl = this_.attr("data-href")
        
        $.ajax({
            url: friendUrl,
            type: "GET",
            data: {},
            success: function(data){
                if (data.friended==true){
                    this_.text("Unfollow");
                    this_.addClass("btn-info")
                    this_.removeClass("btn-outline-info")
                } else {
                    this_.text("Follow");
                    this_.addClass("btn-outline-info")
                    this_.removeClass("btn-info")
                }
                console.log(data);
            },
            error: function(error){
                console.log(error)
                console.log("error")
            }
    
    
        });
    });
});
   
