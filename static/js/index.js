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
                $(".delete-p-btn").click(fc_delete_p);
            }
            $("#projectname").val("");
        });
    });

    var fc_delete_p = function(){
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
    };
    $(".delete-p-btn").click(fc_delete_p);

    $("#addmilestone").click(function(){
        $.post({
            url:"/add_milestone",
            data:{
                name: $("#milestonename").val(),
                pid: $("#milestone-pid").val()
            }
        }).success(function(data){
            if(data.status=="ok"){

                line = "<tr>";
                line += "<td><a href=\"/"+data.object.slug+"/\" data-eid=\""+data.object.eid+"\" class=\"load-p-btn\">"+data.object.name+"</a></td>";
                line += "<td><a href=\"#\" data-eid=\""+data.object.eid+"\" class=\"delete-m-btn\"><i class=\"fa fa-trash-o\"></i></a></td>";
                line += "</tr>";

                $('#tb-milestones > tbody:last-child').append(line);
                $(".delete-m-btn").click(fc_delete_m);
            }
            $("#milestonename").val("");
        });
    });

    var fc_delete_m = function(){
        var tr = $(this).closest('tr');
        $.post({
            url: "/rm_milestone",
            data:{
                mid: $(this).attr("data-eid")
            }
        }).success(function(){
            tr.css("background-color","#FF3700");
            tr.fadeOut(400, function(){
                tr.remove();
            });
            return false;
        });
        return false;
    };
    $(".delete-m-btn").click(fc_delete_m);

    var get_issue_html = function(issue){
        console.log("Adicionando esta:");
        console.log(issue);

        line = "<tr>";
        line += "<td>"+issue.name+"</td>";
        line += "<td>"+issue.milestone.name+"</td>";

        if(issue.status == "backlog"){
            line += "<td class=\"text-center colicon text-muted\" title=\"Backlog\">";
            line += "<i class=\"fa fa-bars\"></i>";
        }else if(issue.status == "programada"){
            line += "<td class=\"text-center colicon\" title=\"Programada\">";
            line += "<i class=\"fa fa-crosshairs\"></i>";
        }else if(issue.status == "emandamento"){
            line += "<td class=\"text-center colicon text-success\" title=\"Em andamento\">";
            line += "<i class=\"fa fa-play\"></i>";
        }else if(issue.status == "concluida"){
            line += "<td class=\"text-center colicon text-muted\" title=\"Concluída\">";
            line += "<i class=\"fa fa-thumbs-o-up\"></i>";
        }else{
            line += "<td class=\"text-center colicon text-muted\">-";
        }
        line += "</td>";


        if(issue.priority == "alta"){
            line += "<td class=\"text-center colicon text-danger\">";
            line += "<i class=\"fa fa-arrow-up\"></i>";
        }else if(issue.priority == "media"){
            line += "<td class=\"text-center colicon\">";
            line += "<i class=\"fa fa-minus\"></i>";
        }else if(issue.priority == "baixa"){
            line += "<td class=\"text-center colicon text-muted\">";
            line += "<i class=\"fa fa-arrow-down\"></i>";
        }else{
            line += "<td class=\"text-center colicon text-muted\">-";
        }
        line += "</td>";


        if(issue.type == "bug"){
            line += "<td class=\"text-center colicon \">";
            line += "<i class=\"fa fa-bug text-info\"></i>";
        }else if(issue.type == "melhoria"){
            line += "<td class=\"text-center colicon\">";
            line += "<i class=\"fa fa-plus text-info\"></i>";
        }else if(issue.type == "tarefa"){
            line += "<td class=\"text-center colicon text-muted\">";
            line += "<i class=\"fa fa-tasks text-info\"></i>";
        }else{
            line += "<td class=\"text-center colicon text-muted\">-";
        }
        line += "</td>";


        line += "</tr>";

        return line;
    };

    $("#btn-add-issue").click(function(){
        var name = $("#issuename").val();
        var pid = $("#pid").val();
        var issue_type = $("#type").val();
        var priority = $("#priority").val();
        var milestone = $("#milestone").val();
        var status = $("#status").val();

        $.post({
            url:"/add_issue",
            data:{
                name: name,
                pid: pid,
                mid: milestone,
                priority: priority,
                status: status,
                type: issue_type
            }
        }).success(function(data){
            if(data.status=="ok"){

                var milestoneatual = $("#mid").val()
                if(milestoneatual == data.object.milestone.eid){
                    $('#tb-issues > tbody:last-child').append(get_issue_html(data.object));
                }
            }
            $("#milestonename").val("");
        });

    });

    var fc_delete_m = function(){
        var tr = $(this).closest('tr');
        $.post({
            url: "/rm_milestone",
            data:{
                mid: $(this).attr("data-eid")
            }
        }).success(function(){
            tr.css("background-color","#FF3700");
            tr.fadeOut(400, function(){
                tr.remove();
            });
            return false;
        });
        return false;
    };
    $(".delete-m-btn").click(fc_delete_m);

});
