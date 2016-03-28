$(document).ready(function(){

    $("#addproject").click(function(){
        $.post({
            url:"/add_project",
            data:{
                name: $("#projectname").val()
            }
        }).success(function(data){
            if(data.status=="ok"){

                line = "<tr>";
                line += "<td><a href=\"/"+data.object.slug+"/\" data-eid=\""+data.object.eid+"\" class=\"load-p-btn\">"+data.object.name+"</a></td>";
                line += "<td><a href=\"#\" data-eid=\""+data.object.eid+"\" class=\"delete-p-btn\"><i class=\"fa fa-trash-o\"></i></a></td>";
                line += "</tr>";

                $('#tb-projetos > tbody:last-child').append(line);
            }
            $("#projectname").val("");
        });
    });

    $(".delete-p-btn").click(function(){
        var tr = $(this).closest('tr');
        $.post({
            url: "/rm_project",
            data:{
                pid: $(this).attr("data-eid")
            }
        }).success(function(){
            console.log("Deletado!");
            tr.css("background-color","#FF3700");
            tr.fadeOut(400, function(){
                tr.remove();
            });
            return false;
        });
        return false;
    });

});
