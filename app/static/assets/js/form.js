console.log("cargue el arc")

$(document).ready(function(){
   
    $('form').on('submit', function(event){
        
        $.ajax({
            data: {
                stat_date : $("#start_date").val(),
                end_date : $("#end_date").val()
            },   
            type : 'POST',
            url : '/predict'  
        })
        event.preventDefault();

    });

console.log(start_date)
});