function makeTabs(group) {
        var name  = group['name'];
        var title = group['title'];
        var graphs= group['graphs'];

        var code = "<h2>"+title+"</h2>\n";
        code += "<ul class=\"nav nav-tabs\">\n";
        //var code = "<ul class=\"tab\">\n";
        graphs.map(function(g,i){
		if (i === 0) {
                	code += "<li class=\"active\"><a data-toggle=\"tab\"  href=\"#"+g['name']+"\>"+g['title']+"</a></li>\n";
                	//code += "<li><a href=\"javascript:void(0)\" class=\"tablinks\" onclick=\"openTab(event, \'"+g['name']+"\')\" id=\"defaultOpen\">"+g['title']+"</a></li>\n";
		} else {
                	code += "<li><a data-toggle=\"tab\"  href=\"#"+g['name']+"\>"+g['title']+"</a></li>\n";
                	//code += "<li><a href=\"javascript:void(0)\" class=\"tablinks\" onclick=\"openTab(event, \'"+g['name']+"\')\">"+g['title']+"</a></li>\n";
		}
        });
        code += "</ul>\n\n";
        return code;
}

function renderGraph(graph) {
        var name  = graph['name'];
        var title = graph['title'];
        var url   = graph['url'];

        var code = "<div id=\"" + name + "\" class=\"django-collectd-rest-graph\">\n";
        code += "<h3>" + title + "</h3>\n";
        code += "<img src=" + url + " />\n";
        code += "</div>\n";
        return code;
}

function renderGroup(group) {
        var name  = group['name'];
        var title = group['title'];
        var graphs= group['graphs'];

        var code = "<div class=\"tab-content\">\n";
        graphs.map(function(g,i){
		if (i === 0) {
			code += "<div id=\""+g['name']+"\" class=\"tab-pane fade in active\">\n";
		} else {
			code += "<div id=\""+g['name']+"\" class=\"tab-pane fade\">\n";
		}
                code +=  renderGraph(g) + "\n</div>\n";
        });
        code += "</div>\n";
        return code;
}

$(document).ready(function(){

        $.get( "/collectd_rest/groups/", function( data ) {
                data.forEach(function(entry) {
                        var name = entry['name'];
                        var code= "<div class=\"container\">"
			code += makeTabs(entry);
			code += renderGroup(entry);
			code += "</div>";
                        $(".django-collectd-rest-group#" + name).html(code);
                });
        });

});
