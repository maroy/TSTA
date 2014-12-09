var interval_id = null;
var clusterRuns = null;
var currentClusterIndex = null;
var trends = null;

function TICKLEN() {
    return 500;
}

function sortMap(map, fn) {
    var keys = Object.keys(map);

    var cl = function(lKey, rKey) {
        return fn(map[lKey], map[rKey]);
    };

    var result = [];
    var sorted_keys = keys.sort(cl);
    for (var i=0; i<sorted_keys.length; i++ ) {
        var key = sorted_keys[i];
        result.push({
            k: key,
            v: map[key]
        });
    }

    return result;
}

function Cluster(raw) {
    var self = this;

    self.percentage = raw["percentage"];
    self.words = raw["words"];
}

function ClusterRun(raw) {
    var self = this;

    var date_strs = raw["date"].split(' - ');

    self.start_date = new Date(Date.parse(raw["start_date"]));
    self.end_date = new Date(Date.parse(raw["end_date"]));

    self.clusters = {};
    $.each(raw["clusters"], function(idx, value) {
        var cluster = new Cluster(value)
        self.items[cluster.center](cluster);
    });
}

function ClusterRuns(raw) {
    var self = this;

    self.items = []
    $.each(raw, function(idx, rawRun) {
        self.items.push(new ClusterRun(rawRun));
    })
}

function KeyWord(keyWord) {
    var self = this;

    self.word = keyWord;
    self.score = 1;
}

function Trend(keyWord, supportingKeyWords) {
    var self = this;
    self.keyWord = new KeyWord(keyWord);

    self.supportingKeyWords = {};
    $.each(supportingKeyWords, function(idx, word) {
        self.supportingKeyWords[word] = new KeyWord(word);
    });

    self.handleOccurrence = function(cluster) {
        self.KeyWord.score++;

        var newKeywordsInCluster = cluster.supportingKeyWords.slice(0);

        $.each(cluster.supportingKeyWords, function(idx, word) {
            if (word in self.supportingKeywords) {
                self.supportingKeywords[word].score++;

            } else {
                self.supportingKeyWords[word] = new KeyWord(word);         
            }
        });
    }
}

function TrendSet() {
    var self = this;
    self.items = [];

    self.handleRun = function(clusterRun) {
    }
}

function updateTrendSetDisplay(clusterRun) {
    $dateRange = $('#dateRange');
    $dateRange.html(formatDate(clusterRun.startDate) + ' - ' + formatDate(clusterRun.endDate));

    $trendTableBody = $('#trendTable tbody');

    var tableData = [];
    tableData.push([
        Math.round(clusterRun.items[0].percentage * 100.0) + "%",
        Math.round(clusterRun.items[1].percentage * 100.0) + "%",
        Math.round(clusterRun.items[2].percentage * 100.0) + "%"
    ]);
    tableData.push([
        clusterRun.items[0].topKeyWord,
        clusterRun.items[1].topKeyWord,
        clusterRun.items[2].topKeyWord
    ]);
    for (var i=0; i<9; i++) {
        tableData.push([
            clusterRun.items[0].supportingKeyWords[i],
            clusterRun.items[1].supportingKeyWords[i],
            clusterRun.items[2].supportingKeyWords[i]
        ]);
    }

    $trendTableBody.empty();
    for (var r=0; r<tableData.length; r++) {
        var row = tableData[r];
        $tr = $('<tr />')
        for (var c=0; c<row.length; c++ ) {
            $tr.append($('<td />').html(row[c]));
        }
        $trendTableBody.append($tr)
    }
    console.dir(tableData);

}

function loadClusterRuns(subset, cb) {
    $.getJSON('data/' + subset + '.json', function (data, status, jqXHR) {
        var runs = new ClusterRuns(data);
        cb(runs);
    });    
}

function tick() {

    if(currentClusterIndex >= clusterRuns.items.length) {
        stop();
        return;
    }

    var run = clusterRuns.items[currentClusterIndex++];
    trends.handleRun(run);
    updateTrendSetDisplay(run);
}

function stop() {
    clearInterval(interval_id);
    interval_id = null;
    currentClusterIndex = null;
}

function start(startIdx) {
    clear();
    currentClusterIndex = startIdx;
    tick();
    interval_id = setInterval(tick, TICKLEN());    
}

function clear() {
    trends = new TrendSet();
    $('#dateRange').empty();
    $('#trendTable tbody').empty();
}

function formatDate(dt) {
    return moment(dt).format('ddd, MMM Do YYYY, h:mm a');
}

function updateClusterRuns() {
    var subset = $('#subset').val();
    var $startDate = $('#startDate');

    loadClusterRuns(subset, function(runs) {
        clusterRuns = runs;
        $startDate.empty();
        $.each(clusterRuns.items, function(idx, run) {
            var dateStr = formatDate(run.endDate);
            $startDate.append($('<option />').html(dateStr).val(idx))  
        });
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
    updateClusterRuns();
}

$(function() {
    $('#subset').on('change', subsetChanged)
    $('#go').on('click', goClicked)
});