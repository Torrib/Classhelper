//on load
$(document).ready(function()
{
    $(".collapsible").hide();
});

$(document).ready(function()
{
    $("#flip").click(function()
    {
        $("#optional-icon").toggleClass("icon-chevron-up");
        $("#panel").slideToggle("fast");
    });
});

function initChocen()
{
    $(".chzn-select").chosen({disable_search_threshold: 10});
}

//Search
$(document).ready(function()
{
    var rows = $("#subjectTable tbody tr:visible");
    var searchField = $("#searchInput");
    searchField.keyup(function()
    {
        rows.hide();
        if(searchField.val())
        {
            var row = $("td:Contains('" + searchField.val() + "')").closest("tr");
            row.show();
        }
        else
        {
            rows.show();
        }
    });
});

//Tags
function initTags()
{
    var rows = $("#subjectTable tbody tr");
    var tagList = [];
    
    $.getJSON("/classhelper/jsonsubjects", function(json)
    {
        var subjects = json;
        $(".label").click(function(event)
        {
            var clicked = event.target.id;
            if(tagList.indexOf(clicked) > -1)
            {
                tagList.splice(tagList.indexOf(clicked), 1);
            }
            else
            {
                tagList.push(clicked);
            }

            rows.hide()
            for(var i=0; i<subjects.length; i++)
            {
                if(contains(tagList, subjects[i].fields.tags))
                {
                    var row = $("td").filter(function()
                    {  
                        return $(this).text() == subjects[i].fields.subject_code;
                    }).closest("tr");
                    row.show();
                }            
            }
            $(this).toggleClass('label-success');
        });
    });
}

function initRatings()
{
    results = $(".result").each(function()
    {
        value = $(this).text();
        if(value == "0")
        {
            $(this).text("-");
        }
        else if(value.match(/[1-3]/))
        {
            $(this).css('color', 'red');
        }
        else if(value.match(/[4-6]/))
        {
            $(this).css('color', 'orange');
        }
        
        if(value.match(/[7-9]/) || value == "10")
        {
            $(this).css('color', 'green');
        }
    });
}

function initGraph(id)
{
    $.getJSON("/classhelper/jsongrades/",{ subject_id : id }, function(json)
    {
        grades = json;
        drawGraph();
        drawButtons();
        $(".btn-graph").first().addClass('active');
    });
}

function drawGraph()
{
    data = grades[0];
    $.jqplot.config.enablePlugins = true;
    var s1 = [data.fields.a, data.fields.b, data.fields.c, data.fields.d, data.fields.e, data.fields.f]
    var ticks = ['A', 'B', 'C', 'D', 'E', 'F'];
    graph = $.jqplot('grades-graph', [s1],
    {
        seriesColors: [ "#00CC00", "#00CC33", "#CCFF33", "#FFFF00", "#FF6600", "#CC0000"],
        
        seriesDefaults:
        {
            renderer:$.jqplot.BarRenderer,
            pointLabels: { show: true },
            rendererOptions: { barMargin: 2, varyBarColor: true},
        },
        axes:
        {
            xaxis: 
            {
                renderer: $.jqplot.CategoryAxisRenderer,
                ticks: ticks,
                tickOptions: { showGridLine: false },
            },
            yaxis:
            {
                tickOptions: { show: false}
            }
        },
        grid:{ gridLineColor: '#FFF',}
    });
}

function drawButtons()
{
    for(i=0; i<grades.length;i++)
    {
        $("#grades-buttons").append($('<a class="btn btn-graph" id=' + i + '>' + grades[i].fields.semester_code + '</a>'));
        if((i % 3) == 0 && i > 0)
        {
            $("#grades-buttons").append('</br>');
        }
    }
    $(".btn-graph").bind('click', function(event)
    {
        $(".btn-graph").removeClass("active");
        clicked = event.target.id
        $(event.target).addClass('active');
        changeGraphData(grades[clicked]);
    });
}

function changeGraphData(data)
{
    s1 = [data.fields.a, data.fields.b, data.fields.c, data.fields.d, data.fields.e, data.fields.f];
    graph.replot( {data:[s1]});
}

//Help methods
function contains(activeTags, subjectTags)
{
    for(var i=0; i < activeTags.length; i++)
    {
        if(subjectTags.indexOf(parseInt(activeTags[i])) == -1)
        {
            return false;
        }
    }
    return true;
}

jQuery.expr[":"].Contains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});


//obsolite
$(document).ready(function()
{
    $(".btn-sidepanel").click(function(event)
    {
        clicked = event.target.id;
        $("#" + clicked + "Panel").slideToggle("fast");
        $("#" + clicked).toggleClass('active');
        $("#" + clicked + "Icon").toggleClass('icon-minus');
    });
});
