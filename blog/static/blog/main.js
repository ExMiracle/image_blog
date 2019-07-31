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
                console.log(data);
            },
            error: function(error){
                console.log(error)
                console.log("error")
            }
    
    
        });
    });
});
   
