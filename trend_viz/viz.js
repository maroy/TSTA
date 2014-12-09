var interval_id = null;
var cluster_run_index = null;
var cluster_runs = null;

var current_trends = [{id: 0}, {id: 0}, {id: 0}];

function TICKLEN() {
    var tickLen = parseInt($('#tickLen').val());

    $('#tickLen').css('color', isNaN(tickLen) ? 'red' : 'black');

    if (isNaN(tickLen)) {
        return 250;        
    } else {
        return tickLen;
    }
}

function get_trend(trends, id) {
    for(var i=0; i<trends.length; i++) {
        if (trends[i].id === id) {
            return trends[i];
        }
    }
    return null;
}

function update_trend_display(clusterRun) {

    $dateRange = $('#dateRange');
    var endDate = new Date(Date.parse(clusterRun.end));
    //$dateRange.html(clusterRun.start + ' - ' + clusterRun.end);
    $dateRange.html(endDate.toDateString() + ' ' + endDate.toTimeString());

    $trendTableBody = $('#trendTable tbody');
    $trendTableBody.empty();

    // use a temp map to match the new set of trends with any that are displayed
    var temp = {};
    $.each(clusterRun.trends, function(idx, trend) {
        temp[trend.id] = trend;
    });

    // replace displayed trends with the updated versions, clear out locations for non-matching trends
    $.each(clusterRun.trends, function(idx, trend) {
        if (trend.id in temp) {
            current_trends[idx] = trend;
            delete temp[trend.id];
        } else {
            current_trends[idx] = null;
        }
    });

    // fill in empty columns with new trends
    $.each(temp, function(idx, trend) {
        for (var i=0; i<current_trends.length; i++) {
            if (current_trends[i] === null) {
                current_trends[i] = trend;
                break;
            }
        }
    });

    var tableData = [[],[],[],[],[],[],[],[],[],[],[]];
    var min_score = Number.MAX_VALUE;
    var max_score = 0;
    $.each(clusterRun.trends, function(idx,trend) {
        min_score = Math.min(min_score, trend.score);
        max_score = Math.max(max_score, trend.score);
    });

    $.each(current_trends, function(col, trend) {
        trend = get_trend(clusterRun.trends, trend.id);

        trend.color = trend.score == max_score ? "green" : trend.score == min_score ? "red" : "yellow";
    });

    
    for (var c=0; c<3; c++) {
        var trend = current_trends[c];
        tableData[0].push(
            '<strong style="color: ' + trend.color + '">' + Math.round(trend.score * 1000.0) + "</strong>"
        );
        for (var j=0; j<10; j++) {
            tableData[j+1].push(current_trends[c].words[j]);
        }
    }

    $trendTableBody.empty();
    for (var r=0; r<tableData.length; r++) {
        var row = tableData[r];
        $tr = $('<tr />');
        for (c=0; c<row.length; c++ ) {
            if (r === 0) {
                $tr.append($('<td />').html(row[c]).css('background-color', 'black'));
            } else {
                $tr.append($('<td />').html(row[c]).css('background-color', randomColorForWord(row[c])));
            }
            
        }
        $trendTableBody.append($tr);
    }
}

var word_colors = {};
function randomColorForWord(word) {
    if (!(word in word_colors)) {

        // credit: http://www.paulirish.com/2009/random-hex-color-code-snippets/
        word_colors[word] = '#'+Math.floor(Math.random()*16777215).toString(16);
    }
    return word_colors[word];
}

function load_cluster_runs(subset, cb) {
    $.getJSON('data/trends_' + subset + '.json', function (data, status, jqXHR) {
        cb(data);
    });    
}

function tick() {

    if(cluster_run_index >= cluster_runs.length) {
        stop();
        return;
    }

    var run = cluster_runs[cluster_run_index++];
    update_trend_display(run);
}

function stop() {
    clearInterval(interval_id);
    interval_id = null;
    current_cluster_index = null;
}

function start(start_idx) {
    clear();
    cluster_run_index = start_idx;
    tick();
    interval_id = setInterval(tick, TICKLEN());    
}

function clear() {
    $('#dateRange').empty();
    $('#trendTable tbody').empty();
}

function formatDate(dt) {
    return moment(dt).format('ddd, MMM Do YYYY, h:mm a');
}

function load_data() {
    var subset = $('#subset').val();
    var $startDate = $('#startDate');

    load_cluster_runs(subset, function(runs) {
        cluster_runs = runs;
        $startDate.empty();
        $.each(cluster_runs, function(idx, run) {
            $startDate.append($('<option />').html(run.end).val(idx));
        });
        $('#loading').hide();
    });
}

function goClicked() {
    var subset = $('#subset').val();
    var startIdx = $('#startDate').val();

    if (subset && startIdx) {
        stop();
        start(startIdx);
    }
}

function startDateChanged() {
    var subset = $('#subset').val();
    var startIdx = $('#startDate').val();

    if (subset && startIdx) {
        stop();
        start(startIdx);
    }
}

function subsetChanged() {
    stop();
    $('#loading').show();
    load_data();
}

$(function() {
    $('#subset').on('change', subsetChanged);
    $('#go').on('click', goClicked);
});